from re import fullmatch
import json

class Checks:
    data_structure = {
        'bus_id': {'type': int, 'required': True},
        'stop_id': {'type': int, 'required': True},
        'stop_name': {'type': str, 'required': True, 'format': '^[A-Z][A-Za-z\s]+(Road|Avenue|Boulevard|Street)$'},
        'next_stop': {'type': int, 'required': True},
        'stop_type': {'type': str, 'required': False, 'format': '[SOF]?'},
        'a_time': {'type': str, 'required': True, 'format': '[0-2][0-9]:[0-5][0-9]'}
    }

    def __init__(self, data):
        self.data = data
        self.structure_errors = {key:0 for i in self.data for key in i}
        self.format_errors = {key:0 for i in self.data for key in i}

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
        for k, v in self.structure_errors.items():
            print(k, v)

    def validate_format(self):
        for item in self.data:
            for field, value in item.items():
                format_pattern = self.data_structure.get(field).get('format')
                if format_pattern and not fullmatch(str(format_pattern), str(value)):
                    self.format_errors[field] += 1

        print(f'Format validation: {sum(self.format_errors.values())} errors')
        for k, v in self.format_errors.items():
            if k in ('stop_name', 'stop_type', 'a_time'):
                print(k, v)

def main():
    # The string containing the data in JSON format is passed to standard input.
    data = json.loads(input())
    Checks(data).validate_format()

if __name__ == '__main__':
    main()
