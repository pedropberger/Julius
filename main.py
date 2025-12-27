from modules.portaltp import run as run_portaltp

def main():
    print("Starting data extraction...")
    run_portaltp.run()
    print("Data extraction finished.")

if __name__ == "__main__":
    main()