import json


class Checks:
    '''
    bus_id: int  # req
    stop_id: int  # req
    stop_name: str  # req
    next_stop: int  # req
    stop_type: chr  # S O F
    a_time: str  # HH:MM req
    '''
    def __init__(self, data):
        self.data = data
        self.structure_errors = {key:0 for i in self.data for key in i}

    def validate_structure(self):
        for item in self.data:
            for field, value in item.items():
                if field == 'stop_name' or field == 'a_time':
                    if not isinstance(value, str) or value == '':
                        self.structure_errors[field] += 1
                elif field == 'stop_type':
                    if not isinstance(value, str) or len(value) > 1:
                        self.structure_errors[field] += 1
                else:
                    if not isinstance(value, int) or value == '':
                        self.structure_errors[field] += 1

        print(f'Type and required field validation: {sum(self.structure_errors.values())} errors')
        for k, v in self.structure_errors.items():
            print(k, v)

def main():
    # The string containing the data in JSON format is passed to standard input.
    data = json.loads(input())
    Checks(data).validate_structure()

if __name__ == '__main__':
    main()
