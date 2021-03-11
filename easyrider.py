import itertools
import json
from collections import Counter
from re import fullmatch

# A lot of dirty code, but there's no reason to rewrite it
# This project just a bunch separate, poorly described puzzles
class Checks:
    data_structure = {
        'bus_id': {'type': int, 'required': True},
        'stop_id': {'type': int, 'required': True},
        'stop_name': {'type': str, 'required': True, 'format': '^[A-Z][A-Za-z]+(Road|Avenue|Boulevard|Street)$'},
        'next_stop': {'type': int, 'required': True},
        'stop_type': {'type': str, 'required': False, 'format': '[SOF]?'},
        'a_time': {'type': str, 'required': True, 'format': '[0-2][0-9]:[0-5][0-9]'}
    }

    def __init__(self, data):
        self.data = data
        self.structure_errors = {key: 0 for i in self.data for key in i}
        self.format_errors = {key: 0 for i in self.data for key in i}

    def validate_structure(self):
        for item in self.data:
            for field, value in item.items():

                # check type
                if not isinstance(value, self.data_structure.get(field).get('type')):
                    self.structure_errors[field] += 1
                    continue  # Either a "required", or a "type" error counts, but not both at the same time!

                # check required fields
                if self.data_structure.get(field).get('required') and value == '':
                    self.structure_errors[field] += 1

                # check stop_type
                if field == 'stop_type' and len(str(value)) > 1:
                    self.structure_errors[field] += 1

        print(f'Type and required field validation: {sum(self.structure_errors.values())} errors')
        print('\n'.join(f'{field}: {err_count}' for field, err_count in self.structure_errors.items()))

    def validate_format(self):
        for item in self.data:
            for field, value in item.items():

                # check format
                format_pattern = self.data_structure.get(field).get('format')
                if format_pattern and not fullmatch(str(format_pattern), str(value)):
                    self.format_errors[field] += 1

        print(f'Format validation: {sum(self.format_errors.values())} errors')
        for k, v in self.format_errors.items():
            if k in ('stop_name', 'stop_type', 'a_time'):
                print(k, v)

    def bus_line_info(self):
        lines = Counter(b['bus_id'] for b in self.data)
        print('Line names and number of stops:')
        print('\n'.join(f'bus_id: {line}, stops: {stops}' for line, stops in lines.items()))
        return lines

    def bus_start_stop_check(self):
        stops = {}
        for item in self.data:
            stops.setdefault(item['bus_id'], [])
            stops.get(item['bus_id']).append(item['stop_type'])
        for bus, stop in stops.items():
            if 'S' not in stop or 'F' not in stop:
                print(f'There is no start or end stop for the line: {bus}.')
                return False
        return True

    def bus_stops_count(self):
        stops = {}
        starts = set()
        ends = set()
        for item in self.data:
            stops.setdefault(item['stop_type'], [])
            stops.get(item['stop_type']).append(item['stop_name'])

        for stop_type, stop_name in stops.items():
            if stop_type == 'S':
                for i in stop_name:
                    starts.add(i)
            if stop_type == 'F':
                for i in stop_name:
                    ends.add(i)

        transfers = self.transfer_stops()

        print(f'Start stops: {len(starts)} {sorted(list(starts))}')
        print(f'Transfer stops: {len(transfers)} {sorted(list(transfers))}')
        print(f'Finish stops: {len(ends)} {sorted(list(ends))}')
        return starts, transfers, ends

    def transfer_stops(self):
        stops = {}
        transfers = set()
        for item in self.data:
            stops.setdefault(item['bus_id'], [])
            stops.get(item['bus_id']).append(item['stop_name'])

        for item in itertools.combinations(stops.values(), 2):
            transfer = (set(item[0]).intersection(item[1]))
            for i in transfer:
                transfers.add(i)
        return transfers

    def time_check(self):
        print('Arrival time test:')
        stops = []
        time_error = 0
        for item in self.data:
            stops.append((item['bus_id'], item['a_time'], item['stop_name']))

        prev_time = ''
        prev_bus = ''
        for stop in stops:
            bus_id = stop[0]
            bus_time = stop[1]
            stop_name = stop[2]

            if prev_time != '' and bus_time <= prev_time and prev_bus == bus_id:
                print(f'bus_id line {bus_id}: wrong time on station {stop_name}')
                time_error += 1
                # check for next bus_id
                prev_bus *= 2
                prev_time = ''

            if time_error == 0 and bus_id != prev_bus:
                prev_bus = bus_id
            if prev_bus == bus_id:
                prev_time = bus_time

        if time_error == 0:
            print('OK')

    def on_demand_check(self):
        starts, transfers, ends = self.bus_stops_count()
        on_demand_stops = {item['stop_name'] for item in self.data if item['stop_type'] == 'O'}
        stops_with_errors = []

        for i in starts, transfers, ends:
            stops_with_errors.extend(list(on_demand_stops.intersection(i)))

        print('On demand stops test:')
        print(f'Wrong stop type: {sorted(list(set(stops_with_errors)))}' if stops_with_errors else 'OK')


def main():
    # The string containing the data in JSON format is passed to standard input.
    data = json.loads(input())
    check = Checks(data)
    check.on_demand_check()


if __name__ == '__main__':
    main()
