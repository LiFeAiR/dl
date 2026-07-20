import argparse, os, sys, yaml

import fishing
import fighting
import party

def main():
    parser = argparse.ArgumentParser(description='dl playing bot')
    parser.add_argument("-j", "--job", help="Job type")
    parser.add_argument("-a", "--account", help="Account name")
    args = parser.parse_args()

    name, api_id, api_hash = "", "", ""
    config = {}
    with open(os.path.join(sys.path[0], 'config.yaml'), 'r') as file:
        config = yaml.safe_load(file)

    for a in config.get('accounts'):
        if a.get('name') == args.account:
            name, api_id, api_hash = a.get('name'), a.get('api_id'), a.get('api_hash')

    if name == "" or api_id == "" or api_hash == "":
        print("Please enter account name and api_id and api_hash")
        return

    jobs = {
        "fighting": fighting.main,
        "fishing": fishing.main,
        "party": party.main,
    }

    jobs.get(args.job, lambda: "Undefined job type")(name, api_id, api_hash)


if __name__ == '__main__':
    main()
