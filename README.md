# Python link shortener
Building a simple link shortener using Flask
Link shortener using MongoDB as a databace. 

Currently supports POST Request to add shortlink. 
```
curl --request POST \
  --url http://127.0.0.1:5000/addShortLink \
  --header 'content-type: application/json' \
  --data '{
	"shortLink":" Your short link",
	"redirectTo":"where to redirect user",
    "callbackUrl":"where to send link followed data"
}'
```
When smbd follows the link, sends info about it send to ```callbackUrl``` toghether with user agent.

## TO-DO
- [ ] API Documentation
- [ ] Instructions about how to set up it