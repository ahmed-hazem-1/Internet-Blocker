import winreg
import win32com.client
import win32com.client
import os


def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]
    software_dict = {}

    for i in range(count_subkey):
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            name = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            if name in software_dict:
                continue

            version = winreg.QueryValueEx(asubkey, "DisplayVersion")[0] if winreg.QueryValueEx(asubkey,
                                                                                               "DisplayVersion") else 'undefined'
            publisher = winreg.QueryValueEx(asubkey, "Publisher")[0] if winreg.QueryValueEx(asubkey,
                                                                                            "Publisher") else 'undefined'

            try:
                install_location = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
            except EnvironmentError:
                install_location = None

            if install_location:
                software_dict[name] = {
                    'version': version,
                    'publisher': publisher,
                    'install_location': install_location
                }
        except EnvironmentError:
            continue

    return software_dict


def get_installed_apps():
    return {**foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY),
            **foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY),
            **foo(winreg.HKEY_CURRENT_USER, 0)}


def block_program(program_path):
    # Check if the original file path exists
    # TODO: Check if the original file path exists
    if program_path is None or program_path == '':  # FIXME: program_path is None
        print("Program path is None, cannot block the program.")

    elif os.path.exists(program_path):
        print(f"Found the application at: {program_path}")
    else:
        # Convert the path to lowercase and check again
        lower_program_path = program_path.lower()
        if os.path.exists(lower_program_path):
            print(f"Found the application at: {lower_program_path}")
            program_path = lower_program_path
        else:
            print(f"The application '{program_path}' was not found.")
            return  # Exit if not found

    # Proceed to create the firewall rule
    firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")
    rule_name = f"Block {os.path.basename(program_path)}"

    # Check if the rule already exists
    for rule in firewall.Rules:
        if rule.Name == rule_name:
            print("Rule already exists.")
            return

    # Create a new firewall rule
    new_rule = win32com.client.Dispatch("HNetCfg.FWRule")
    new_rule.Name = rule_name
    new_rule.ApplicationName = program_path
    new_rule.Action = 0  # Block
    new_rule.Direction = 2  # Outbound
    new_rule.Profiles = 0x7  # Applies to all profiles
    new_rule.Enabled = True

    try:
        firewall.Rules.Add(new_rule)
        print(f"Blocked {program_path}. Rule Name: {new_rule.Name}")
    except Exception as e:
        print(f"Error blocking program: {str(e)}")


def delete_firewall_rule(app_path):
    firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")
    if app_path is None or app_path == '':  # FIXME: program_path is None
        print("Program path is None, cannot block the program.")
        return
    rule_name = f"Block {os.path.basename(app_path)}"  # Construct the rule name

    rule_found = False  # Flag to check if the rule was found

    # Iterate through the existing rules
    for rule in firewall.Rules:
        if rule.Name == rule_name:
            try:
                firewall.Rules.Remove(rule.Name)
                print(f"Deleted rule: {rule_name}")
                rule_found = True
                break  # Exit the loop once the rule is found
            except Exception as e:
                print(f"Error deleting rule: {str(e)}")
                return  # Exit if an error occurs

    if not rule_found:
        print(f"Rule not found: {rule_name}")
