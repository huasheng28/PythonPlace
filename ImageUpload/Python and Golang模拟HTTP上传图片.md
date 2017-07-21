#Python模拟HTTP上传图片
```
#utf-8
import threading
from time import ctime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
i=0
for i in range(1):
    register_openers()
    datagen, headers = multipart_encode({"file": open("pian1.jpg", "rb")})
    request = urllib2.Request("http://test.seeunsee.cn/jsb/wm-test/api/check.php", datagen, headers)
    i+=1
    print urllib2.urlopen(request).read(),i
```
#Golang模拟HTTP上传图片
```
package main
import (
	"bytes"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
)

// Creates a new file upload http request with optional extra params
func newfileUploadRequest(uri string, params map[string]string, paramName, path string) (*http.Request, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile(paramName, filepath.Base(path))
	if err != nil {
		return nil, err
	}
	_, err = io.Copy(part, file)

	for key, val := range params {
		_ = writer.WriteField(key, val)
	}
	err = writer.Close()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", uri, body)
	req.Header.Set("Content-Type", writer.FormDataContentType())
	return req, err
}

func main() {
	path, _ := os.Getwd()//获取当前绝对文件路径
	path += "/pian.jpg"
	extraParams := map[string]string{
		"id":               "WU_FILE_0",
		"name":             "pian.jpg",
		"type":             "image/jpeg",
		"lastModifiedDate": "Mon Apr 17 2017 15:31:08 GMT+0800 (CST)",
		"size":             "241281",
	}
	request, err := newfileUploadRequest("http://test.seeunsee.cn/jsb/wm-test/api/check.php", extraParams, "file", path)
	if err != nil {
		log.Fatal(err)
	}
	client := &http.Client{}
	resp, err := client.Do(request)
	if err != nil {
		log.Fatal(err)
	} else {
		body := &bytes.Buffer{}
		_, err := body.ReadFrom(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		resp.Body.Close()
		//fmt.Println(resp.StatusCode)
		//fmt.Println(resp.Header)
		fmt.Println(body)
	}
}
```