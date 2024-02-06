# Emotion Analysis Server Documentation

## Specifications

Required Libraries:

- torch
- transformers
- pandas

## Configuration

- IP address : localhost
- Port : 8081 `<configurable>`

## Request Object

Parameters:

1. message_id
    - Data type : str
    - Description : action to be performed on input
    - Mandatory : yes

2. message
    - Data type : str
    - Description : text provided by the user
    - Mandatory : yes if message_id is 'add_emotion_markups'

3. country
    - Data type : str
    - Description : name of the country of the user iso-country code
    - Mandatory : yes if message_id is 'add_emotion_markups'

4. speech_rate
    - Data type : float
    - Description : time taken for avatar gesture completion
    - Mandatory : no
    - Default : 1.5

5. avatar_type
    - Data type : str
    - Description : avatar body type
    - Mandatory : no
    - Default : "full"

6. session_details
    - Data type : json
    - Description : details of session
    - Mandatory : no

7. previous_markup
    - Data type : str
    - Description : last markup of the previous response
    - Mandatory : no

Example: 

    {
        'message_id':'add_emotion_markups',
        'message':"Hello friends, a warm welcome from India. As the leader of SpringCT, I stand before you with a sense of excitement and anticipation.",
        'country':'ind',
        'speech_rate':1.5,
        'avatar_type':"full",
        'session_details':{
            'session_id':'',
            'avatar_id':''
        },
        'previous_markup':"<base,happy>"
    }

## Response Object

Parameters:

1. message_id
    - Data Type : str
    - Descripton : message id of the response

2. message
    - Data Type : str
    - Description : message with added emotion markups (is provided only when message_id of request object is 'add_emotion_markups')

3. status_code
    - Data Type : int
    - Description : status code of the response

4. response_message
    - Data Type : str
    - Description : response message
    
Example:
    
    {
        'message_id':"add_emotion_markups",
        'status_code':200,
        'response_message':"Emotion markups added successfully.",
        'message': "Hello<mark name="base,happy,close_up"/> friends,<break time="450ms"/> a warm<mark name="namaste,happy,close_up"/> welcome from India. As the<mark name="base,happy"/> leader of SpringCT, I stand before you with a<mark name="spread_arms,happy"/> sense of excitement and anticipation.<mark name="base,happy,close_up"/>"
    }

## Websocket Responses

1. On completion of model initialization
    - Message Id : Initialization Complete
    - Status Code : 200 (OK)
    - Response Message : Server is ready to accept messages

    Example:

        {
            'message_id : 'initialization_complete'
            'status_code': 200,
            'response_message' : 'Server is ready to accept messages',
        }

2. When emotion markups are added successfully.
    - Message Id : Message id of the request
    - Status Code : 200 (OK)
    - Response Message : Emotion markups added successfully
    - Message : Message with added markups 

    Example:

        {
            'message_id' : 'add_emotion_markups',
            'status_code' : 200,
            'response_message' : 'Emotion markups added successfully',
            'message' :  'Hello<mark name="base,happy,close_up"/> friends,<break time="450ms"/> a warm<mark name="namaste,happy,close_up"/> welcome from India. As the<mark name="base,happy"/> leader of SpringCT, I stand before you with a<mark name="spread_arms,happy"/> sense of excitement and anticipation.<mark name="base,happy,close_up"/>'
        }

3. When one of the fields mentioned in the input is missing.
    - Message Id : Operation Failed
    - Status Code : 400
    - Response Message : Bad Request

    Example:

        {
            'message_id' : 'Operation Failed'
            'status_code': 400,
            'response_message' : 'Input not in correct format',
        }