# Import the json and configparser modules
import configparser
import json
import pathlib as p

DEBUG = False

JSON_FILE = "./hosts.json"
INVENTORY_FILE = "./inventory"
HOSTS_DIRECTORY = "./hosts"

# Define a function to load JSON data from a file
def load_json(file):
    if DEBUG: print("using file: ", file)
    # Open the file in read mode
    with open(file, "r") as f:
        # Load the JSON data and return it
        data = json.load(f)
        return data


# Define a function to write data to a file
def write_inventory(data, file, hosts):
    myfindings = {}
    devices = []
    iplist = []
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    # Loop through the data
    for key, value in data.items():
        # Check if the key is _meta
        if key == "_meta":
            # Skip this key as it is not needed for the hosts file
            myfindings = list(data.items())[0][1]["hostvars"]
            for k in myfindings:
                curdict = myfindings[k]
                # only configure for host entry if there's a host name to work with.
                if curdict["ip"] != curdict["name"]:
                    devices.append(curdict)
                    #if debug: print(curdict)
                iplist.append(curdict["ip"])
            continue
    if DEBUG: print("\nfindings: ", myfindings)
    with open(file, "w") as f:
        # Write the data to the file
        for d in devices:
            # write out individual host entries for anything with a host name.
            f.write("\n[%s]\n" % d["name"])
            f.write("%s\n" % d["ip"])
        # write out all ip's to their own section
        f.write("\n[devices]\n")
        for entry in iplist:
            f.write("%s\n" % entry)
    # create hosts directory
    path = p.Path(hosts)
    if not path.exists(): path.mkdir()


# Define a main function
def main():
    # Get the JSON file name from the user input or use the default
    # json_file = input("Enter the JSON file name: ") or "./hosts.json"
    # Get the INI file name from the user input or use the default
    # ini_file = input("Enter the INI file name: ") or "./hosts.ini"
    # Call the load_json function and get the JSON data
    json_data = load_json(JSON_FILE)
    # print json data
    if DEBUG: print("json data: ", json_data)
    # Call the write_ini function and write the INI data to the file
    write_inventory(json_data, INVENTORY_FILE, HOSTS_DIRECTORY)
    
    # Print a success message
    if DEBUG: print(f"Successfully converted {JSON_FILE} to {INVENTORY_FILE}")


# Check if the script is run as the main module
if __name__ == "__main__":
    # Call the main function
    main()
