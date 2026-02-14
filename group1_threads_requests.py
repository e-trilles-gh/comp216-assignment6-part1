import requests, threading
from time import perf_counter

#url list
img_urls = [
    'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0',
    'https://images.unsplash.com/photo-1485833077593-4278bba3f11f',
    'https://images.unsplash.com/photo-1593179357196-ea11a2e7c119',
    'https://images.unsplash.com/photo-1526515579900-98518e7862cc',
    'https://images.unsplash.com/photo-1582376432754-b63cc6a9b8c3',
    'https://images.unsplash.com/photo-1567608198472-6796ad9466a2',
    'https://images.unsplash.com/photo-1487213802982-74d73802997c',
    'https://images.unsplash.com/photo-1552762578-220c07490ea1',
    'https://images.unsplash.com/photo-1569691105751-88df003de7a4',
    'https://images.unsplash.com/photo-1590691566903-692bf5ca7493',
    'https://images.unsplash.com/photo-1497206365907-f5e630693df0',
    'https://images.unsplash.com/photo-1469765904976-5f3afbf59dfb'
    ]

def download_file(file_url):
    
    #splits the url with '/' as the delimeter 
    #and store it into a list    
    split_url = file_url.split('/')
    
    #extracts the last item from the list
    #and append .png to save it as png file    
    file_name = f'{split_url[-1]}.png'
    
    #joins the file name with the folder name where the downloaded files will
    #be saved    
    path_name = f'download_here/{file_name}' #change the location of download folder
    
    #makes a HTTP GET request
    req = requests.get(file_url, stream=True)

    with open(path_name, 'wb') as fd:
        print(f'downloading {file_name} file...')
        
        #downloads the file into small byte and
        #store it in chunk variable        
        for chunk in req.iter_content(chunk_size=50):
            
            #writes every chunk into a file
            fd.write(chunk)
        print(f'...{file_name} file download completed\n')

def time_counter(func, img_url):
    #records the current time before the download starts
    start = perf_counter()
    
    #calls the function that will be tested
    download_type = func(img_url)
    
    #records the current time when the download ends
    end = perf_counter()
    
    print(f'Time elapsed for {download_type} download: {round(end-start)} seconds\n')    

def sequential_download(img_urls):
    for img_url in img_urls:
        download_file(img_url)
    return 'sequential'

def thread_download(img_urls):
    #holds the list of threads that will be made
    threads = list()
    for img_url in img_urls:
        
        #extracts name for the running thread from url
        thread_name = img_url.split('/')[-1]
        
        #creates thread for the method
        #with url argument        
        th = threading.Thread(
            target = download_file,
            name = thread_name,
            args = (img_url,)
        )
        
        #appends each created thread to the list
        threads.append(th)
        
        #starts the thread after being created
        th.start()
        
    for thread in threads:
        #ensures that all threads are finished before
        #proceeding to the rest of the code        
        thread.join()
    
    return 'thread'

time_counter(sequential_download, img_urls)
time_counter(thread_download, img_urls)