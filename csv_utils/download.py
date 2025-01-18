import os
import requests
import tarfile
import shutil  

def main():       
    download("https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/airline_2m.tar.gz", "airline_2m.tar.gz")    
    download("https://ourairports.com/countries/US/airports.csv", "airports.csv")    


def download(url, filename):
    download_folder = './raw_data'
    final_folder = './csv'

    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)

    file_path = os.path.join(download_folder, filename)

    try:
        with requests.get(url, stream=True, allow_redirects=True) as response:
            response.raise_for_status() 
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):  
                    file.write(chunk)

        process_downloaded_file(file_path, final_folder)
        cleanup_folder(download_folder)  

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
        cleanup_folder(download_folder, error=True) 
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        cleanup_folder(download_folder, error=True) 

def process_downloaded_file(file_path, final_folder):
    filename = os.path.basename(file_path)
    if filename.endswith(".gz"):
        try:
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path=final_folder)
        except tarfile.ReadError as e:
            print(f"Error extracting tar.gz file: {e}")
    else:
        try:
            shutil.move(file_path, os.path.join(final_folder, filename))
        except OSError as e:
            print(f"Error moving file: {e}")

def cleanup_folder(download_folder, error=False):
    try:
        if error:
            print(f"Cleaning up download folder {download_folder} due to an error.")
        shutil.rmtree(download_folder)
        print(f"Download folder '{download_folder}' cleaned up.")
    except FileNotFoundError:
        if not error:
            print(f"Warning: Download folder '{download_folder}' not found during cleanup.")
    except OSError as e:
        print(f"Error cleaning up download folder: {e}")


if __name__ == '__main__':
    main()