import requests
import tarfile
import os
def main():    
    download_folder = './raw_data'
    extraction_folder = './csv_file'


    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(extraction_folder, exist_ok=True)
    url = 'https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/airline_2m.tar.gz'
    r = requests.get(url, allow_redirects=True)

    file_path = os.path.join(download_folder,'airline_2m.tar.gz')
    with open(file_path, 'wb') as file:
        file.write(r.content)
    
    # Ouvre le fichier extrait le CSV et le met dans le fichier courant
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=extraction_folder)
    
if __name__ == '__main__':
    main()