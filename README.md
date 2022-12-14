
# Red Hat Apprentice

The application uses RabbitMQ based Load balancing Flask Application.
You wil require local rabbitMq connection along with erlang installed to run this project locally.

All the mentioned endpoints along with load balancing are setup 


## API Reference

#### Welcome

```http
  GET /Welcme
```

#### Place Order

```http
  GET /order
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `order`      | `json` | Order body with Array of String containing pizza name |

#### Get Order

```http
  GET /getorders
```
#### Get Order By Id

```http
  GET /getorders/<order_id>
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `order_id`      | `string` |Order id to fetch data abased on |



## ENVIRON MENT VARIABLES 
```
MONGO_URL = ""
```

## How to run this locally?

1. Create .env file and insert the mongo URL
2. Create virtual env using 
```
python -m venv env
```
3. For windows start venv 
```
cd ./env/Scripts; ./activate; cd ../../
```
4. Install erlang and rabbitMq locally
5. Start flask server
```
 flask --app app.py --debug run
```
