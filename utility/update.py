import argparse
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from paktrack.vibration import vibration, vibration_data_processor
from paktrack.shock import shock, shock_data_processor


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Pak-Track Utility', usage='%(prog)s [options]',
        argument_default=argparse.SUPPRESS)
    parser.add_argument('--db_host', help='database host', nargs='?')
    parser.add_argument(
        '--db_port', help='database port', nargs='?',
        default=27017, type=int)
    parser.add_argument('--db_name', help='database name', nargs='?')
    parser.add_argument('--db_user', help='database username', default=None)
    parser.add_argument('--db_pass', help='database password', default=None)
    parser.add_argument(
        '--service',
        help='which service[vibration (or) shock] you want to process')
    return parser.parse_args()


def main(args):
    if args.service == "vibration":
        process_vibration(args)
    elif args.service == "shock":
        process_shock(args)
    else:
        print "Invalid service"


def process_vibration(args):
    vib = vibration.Vibration(args.db_host, args.db_port, args.db_name, args.db_user, args.db_pass)
    query = {"is_processed": {"$exists": False}}
    fields = {"_id": 1}
    cursor = vib.get_cursor(query, fields)
    data_processor = vibration_data_processor.VibrationDataProcessor(vib)
    count = 0

    for doc in cursor:
        result = data_processor.pre_process_data(doc['_id'])
        print result
        count += 1

    print "Processed %d vibration events", count


def process_shock(args):
    shock_model = shock.Shock(args.db_host, args.db_port, args.db_name, args.db_user, args.db_pass)
    query = {"is_processed": {"$exists": False}}
    fields = {"_id": 1}
    cursor = shock_model.get_cursor(query,fields)
    data_processor = shock_data_processor.ShockDataProcessor(shock_model)
    count = 0

    for doc in cursor:
         result = data_processor.pre_process_data(doc['_id'])
         print result
         count += 1

    print "Processed %d shock events", count

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
