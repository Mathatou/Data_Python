import csv_utils.clean_data
import csv_utils.download

def main():
    csv_utils.download.main()
    csv_utils.clean_data.main()



if __name__ == "__main__":
    main()