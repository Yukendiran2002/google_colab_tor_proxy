import subprocess
import time

def runn_command(command):
    """Run a shell command."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr}")
        return None

def install_dependencies():
    """Update and install necessary packages."""
    runn_command("sudo apt update")
    runn_command("sudo apt install -y tor netcat curl privoxy")

def configure_tor():
    """Configure Tor settings idempotently."""
    config_file = "/etc/tor/torrc"
    torrc_config = [
        "ControlPort 9051",
        "CookieAuthentication 0",
        "AvoidDiskWrites 1"
    ]

    try:
        with open(config_file, 'r') as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = ""

    # Figure out which lines are missing
    lines_to_add = []
    for line in torrc_config:
        if line not in existing_content:
            lines_to_add.append(line)

    # If there are any missing lines, append them
    if lines_to_add:
        with open(config_file, 'a') as f:
            for line in lines_to_add:
                f.write(line + "\n")

def configure_privoxy():
    """Configure Privoxy to route traffic through Tor."""
    config_file = "/etc/privoxy/config"
    config_line = "forward-socks5t / 127.0.0.1:9050 .\n"

    try:
        with open(config_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if config_line not in content:
        with open(config_file, 'a') as f:
            f.write(config_line)

def start_services():
    """Restart Tor and Privoxy services to apply new configurations."""
    print("Restarting Tor and Privoxy services...")
    runn_command("service tor restart")
    runn_command("service privoxy restart")

def check_proxy_health():
    """Check if the Tor proxy is ready by making a test request."""
    print("Waiting for Tor to bootstrap...")
    test_command = "curl --proxy http://127.0.0.1:8118 -s https://check.torproject.org/"
    
    for i in range(30):
        print(f"Attempt {i + 1}/30: Checking proxy status...", end='\r')
        result = runn_command(test_command)
        if result and "Congratulations. This browser is configured to use Tor." in result.stdout:
            print("✅ Tor proxy is ready and working.")
            return True
        time.sleep(1)
        
    print("❌ Tor proxy failed to start or is not responding.")
    return False

def tor_proxy_setup():
    install_dependencies()
    configure_tor()
    configure_privoxy()
    print("Installation and configuration complete.")
    start_services()
    if check_proxy_health():
        print("Setup complete successfully.")
        print("You can now use privoxy to route traffic through Tor via http://127.0.0.1:8118 or http://localhost:8118.")