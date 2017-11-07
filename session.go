package main

import "C"
import (
    "github.com/go-macaron/session"
    "crypto/rand"
    "math/big"
    "unsafe"
)


const alphanum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

// RandomString returns generated random string in given length of characters.
// It also returns possible error during generation.
func randomString(n int) (string, error) {
	buffer := make([]byte, n)
	max := big.NewInt(int64(len(alphanum)))

	for i := 0; i < n; i++ {
		index, err := randomInt(max)
		if err != nil {
			return "", err
		}

		buffer[i] = alphanum[index]
	}

	return string(buffer), nil
}

func randomInt(max *big.Int) (int, error) {
	rand, err := rand.Int(rand.Reader, max)
	if err != nil {
		return 0, err
	}

	return int(rand.Int64()), nil
}

var _session session.RawStore

//export Init
func Init(path string){
    session_id,_ := randomString(16)
    fp := new(session.FileProvider)
    fp.Init(100000, path)
    _session,_ = fp.Read(session_id)
}

//export Release
func Release() int{
    err := _session.Release()
    if err != nil{
        return 1
    }else{
        return 0
    }
}

//export Set
func Set(key string, value string) {
    _session.Set(key,value)
}

//export GetID
func GetID() unsafe.Pointer{
    cs := C.CString(_session.ID())
    return unsafe.Pointer(cs)
}

func main() {}