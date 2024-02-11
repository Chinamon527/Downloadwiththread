import threading
import requests
import os

url = 'https://rr4---sn-5fo-c33l7.googlevideo.com/videoplayback?expire=1699372167&ei=JwhKZeeVA93Sj-8PsqeQgAc&ip=45.13.237.4&id=o-ACFczqE2x597m_YoQ7RNpAEIXiwsaKDSOVOnjj3AtlgT&itag=22&source=youtube&requiressl=yes&spc=UWF9f8LtY1R556ppEhUXLvLDkMPPR_8&vprv=1&svpuc=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=1104.224&lmt=1684162716352915&fexp=24007246,24350018&beids=24350018&c=ANDROID&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=ANLwegAwRQIhANmZQGL2YItI-4vYb7cJgSno-FrGh_ZWfLVVlm8vOgc1AiAc0MPXHH8n6Befz7OSxHyBpymahxx7stgvJ45b_jykZQ%3D%3D&title=%E0%B9%81%E0%B8%81%E0%B8%A5%E0%B9%89%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%84%E0%B8%B8%E0%B8%87%20%E0%B9%82%E0%B8%88%E0%B8%A3%E0%B8%9A%E0%B8%B8%E0%B8%81%20!!%20(%20%E0%B8%84%E0%B8%A5%E0%B8%B4%E0%B8%9B%E0%B8%99%E0%B8%B5%E0%B9%89%E0%B8%81%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%89%E0%B8%B5%E0%B8%A2%E0%B8%9A%E0%B8%84%E0%B8%A3%E0%B8%B1%E0%B8%9A%20)&redirect_counter=1&rm=sn-4g5ekd7s&req_id=abb7e0df69fda3ee&cms_redirect=yes&cmsv=e&ipbypass=yes&mh=Xk&mip=2001:44c8:42cd:3f72:c826:e401:2046:1f38&mm=31&mn=sn-5fo-c33l7&ms=au&mt=1699350296&mv=m&mvi=4&pcm2cms=yes&pl=44&lsparams=ipbypass,mh,mip,mm,mn,ms,mv,mvi,pcm2cms,pl&lsig=AM8Gb2swRAIgcClg0kHW2iJUP0b2HX7wLwuzQwoAyb1QQSYOXUDspn8CIBcNljqFr5AqhHmlC1GUSheQOsTcbTyTOpMKIzKIJzCI'

num_threads = 12 

def download_chunk(start_range, end_range, thread_id):  
    headers = {'Range': f'bytes={start_range}-{end_range}'} 
    print(f"threads {thread_id}",headers) 
    response = requests.get(url, headers=headers) 
    with open(f'chunk{start_range}-{end_range}.zip', 'wb') as f: 
        total_size = int(response.headers.get('content-length', 0)) 
        for data in response.iter_content(chunk_size=1024): 
            f.write(data) 
            downloaded_size = os.path.getsize(f'chunk{start_range}-{end_range}.zip') 
            percent_complete = (downloaded_size / total_size) * 100 
            print(f'Thread {thread_id} Downloading {downloaded_size} bytes out of {total_size} bytes ({percent_complete:.2f}%)', end='\r')
    print(f'Thread {thread_id} Downloaded {downloaded_size} bytes out of {total_size} bytes ({percent_complete:.2f}%)')

def merge_chunks(output_filename, num_chunks):
    with open(output_filename, 'wb') as output_file: 
        for i in range(num_chunks): 
            chunk_filename = f'chunk{i * chunk_size}-{(i + 1) * chunk_size - 1}.zip' 
            with open(chunk_filename, 'rb') as chunk_file:
                output_file.write(chunk_file.read()) 
            os.remove(chunk_filename) 

response = requests.head(url) 
total_size = int(response.headers['Content-Length']) 
chunk_size = total_size // num_threads 

threads = [] 

for i in range(num_threads):
    start_range = i * chunk_size 
    end_range = start_range + chunk_size - 1 
    thread = threading.Thread(target=download_chunk, args=(start_range, end_range, i))  
    threads.append(thread) 
    thread.start() 

for thread in threads:
    thread.join()

output_directory = 'C://Users//doram//OneDrive//Desktop//OS'
output_filename = os.path.join(output_directory, 'te1st.mp4') 

merge_chunks(output_filename, num_threads)

print(f"ดาวน์โหลดเสร็จสิ้นและบันทึกไฟล์ที่ {output_filename}")