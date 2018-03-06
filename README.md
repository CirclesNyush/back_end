# API Documentation

## Personal Info
| URL | function |
|:-------------:|:-------------:|
| [personal/fetchavatar] | Get the url for user's avatar|

###  Receive Data：
```json
    {
       "email":"",//cyphered email with MD5
    }
```
###  Send Data：
```json
    {
       "status":"", 1 for success,
       "avatar": "", the url for avatar
    }
```

| URL | function |
|:-------------:|:-------------:|
| [personal/updateavatar] | Update the user's avatar|

###  Receive Data：
```json
    {
       "email":"",//cyphered email with MD5
       "avatar" : "" //the uploaded avatar
    }
```
###  Send Data：
```json
    {
       "status":"", 1 for success,
       "avatar": "", the url for avatar
    }

```

| URL | function |
|:-------------:|:-------------:|
| [personal/getinfo] | get user's detail info|

###  Receive Data：
```json
    {
       "email":"",//cyphered email with MD5
    }
```
###  Send Data：
```json
    {
       "status":"", 1 for success,
       "data": {
        "avatar": ""         //url for avatar,
         "nickname": ""     //user's nickname,
         "phone": ""        //user's phone number
          "tags":tags       // tags is a JSON Array
       }
    }
```
| URL | function |
|:-------------:|:-------------:|
| [personal/updateinfo] | Update the user's info|

###  Receive Data：
```json
    {
       "email":"",      //cyphered email with MD5.
       "data" : data    // data is a json for all the changes with corresponding category.
    }
```
###  Send Data：
```json
    {
       "status":"", \\1 for success,
       "data": "",  \\ nothing yet
    }

```
