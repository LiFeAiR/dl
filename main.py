import argparse, os, sys, yaml
import inspect

import fishing
import fighting
import party
import terrarium

def main():
    parser = argparse.ArgumentParser(description='dl playing bot')
    parser.add_argument("-j", "--job", help="Job type")
    parser.add_argument("-a", "--account", help="Account name")
    parser.add_argument("-o", "--options", help="Варианты команд")
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

    options = args.options.split(',') if args.options else []

    jobs = {
        "fighting": fighting.main,
        "fishing": fishing.main,
        "party": party.main,
        "terrarium": terrarium.main,
    }

    job = jobs.get(args.job)
    if job:
        sig = inspect.signature(job)
        data = {"name": name, "api_id": api_id, "api_hash": api_hash, "options": options}
        filtered_args = {k: v for k, v in data.items() if k in sig.parameters}
        job(**filtered_args)
    else:
        print(f"Undefined job type {args.job}")


if __name__ == '__main__':
    main()
