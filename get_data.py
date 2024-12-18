import requests


def main():    
    url = 'https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/airline_2m.tar.gz'
    r = requests.get(url, allow_redirects=True)

    file_path = 'airline_2m.tar.gz'
    with open(file_path, 'wb') as file:
        file.write(r.content)
    
    

if __name__ == '__main__':
    main()