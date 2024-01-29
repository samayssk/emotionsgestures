from enum import Enum

class STATUSCODES(int,Enum):
    OK=200
    BAD_REQUEST=400

class RESPONSES(str,Enum):
    INITIALIZATION_COMPLETE="Server is ready to accept messages"
    CONVERTED="Emotion markups added successfully"
    BAD_REQUEST="Bad Request"
