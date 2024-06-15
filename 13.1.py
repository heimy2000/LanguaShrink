import chardet

def detect_encoding_in_chunks(file_path, chunk_size=1024*1024):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            result = chardet.detect(chunk)
            print(result)

detect_encoding_in_chunks('output6.csv')