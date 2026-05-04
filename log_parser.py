import re
from datetime import datetime
from collections import defaultdict

class LogParser:
    def __init__(self, enviados_log='enviados.log', errores_log='errores.log'):
        self.enviados_log = enviados_log
        self.errores_log = errores_log

    def parse_log_file(self, filepath):
        """Parse log file and extract batches with timestamps"""
        batches = []
        current_batch = None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()

                # Match header: "--- Envío 20260504_120000 ---" or "--- Errores 20260504_120000 ---"
                match = re.match(r'^--- (?:Envío|Errores) (\d{8}_\d{6}) ---$', line)
                if match:
                    if current_batch:
                        batches.append(current_batch)
                    timestamp_str = match.group(1)
                    # Parse YYYYMMDD_HHMMSS to datetime
                    dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    current_batch = {
                        'timestamp': dt,
                        'timestamp_str': timestamp_str,
                        'emails': []
                    }
                elif current_batch and line and not line.startswith('---'):
                    # Email line
                    current_batch['emails'].append(line)

            # Add last batch
            if current_batch:
                batches.append(current_batch)

        except FileNotFoundError:
            return []

        return batches

    def get_statistics(self):
        """Get aggregated statistics from both logs"""
        enviados_batches = self.parse_log_file(self.enviados_log)
        errores_batches = self.parse_log_file(self.errores_log)

        total_sent = sum(len(b['emails']) for b in enviados_batches)
        total_errors = sum(len(b['emails']) for b in errores_batches)

        success_rate = (total_sent / (total_sent + total_errors) * 100) if (total_sent + total_errors) > 0 else 0

        return {
            'total_sent': total_sent,
            'total_errors': total_errors,
            'success_rate': round(success_rate, 2),
            'total_batches': len(enviados_batches)
        }

    def get_history(self):
        """Get detailed history combining both logs"""
        enviados_batches = self.parse_log_file(self.enviados_log)
        errores_dict = defaultdict(list)

        # Map errors by timestamp
        errores_batches = self.parse_log_file(self.errores_log)
        for batch in errores_batches:
            errores_dict[batch['timestamp_str']] = batch['emails']

        # Combine history
        history = []
        for batch in enviados_batches:
            ts_str = batch['timestamp_str']
            errors_in_batch = errores_dict.get(ts_str, [])
            sent = len(batch['emails'])
            failed = len(errors_in_batch)
            total = sent + failed
            success_rate = (sent / total * 100) if total > 0 else 0

            history.append({
                'timestamp': batch['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'sent': sent,
                'failed': failed,
                'total': total,
                'success_rate': round(success_rate, 2),
                'failed_emails': errors_in_batch
            })

        # Sort by timestamp descending (newest first)
        history.sort(key=lambda x: x['timestamp'], reverse=True)
        return history
