const WebSocket = require('ws');
const {stdin,stdout}=require('process');
const readline = require('readline').createInterface({input:process.stdin,output:process.stdout});
const ip="localhost";
const port=8081

const ws_address="ws://"+ip+":"+port;

const MessageIds={
    INITIALIZATION_COMPLETE:"initialization_complete",
    ADD_EMOTION_MARKUPS:"add_emotion_markups",
}

const StatusCodes = {
    OK: 200,
    BAD_REQUEST:400,
};

const ResponseMessages = {
    INITIALIZATION_COMPLETE: "Server is ready to accept messages",
    ADD_EMOTION_MARKUPS: "Emotion markups added successfully",
    BAD_REQUEST:"Bad Request",
};

const CountryCodes={
    IND:"ind",
};

const SpeechRates={
    MED:"med",
};

const AvatarTypes={
    HALF:"half",
    FULL:"full",
};

const previous_markup='<base,happy>';

const session_details={};

function handle_input(client){
    readline.question("Enter text: ", async (text) => {
        const input = {
          message_id: MessageIds.ADD_EMOTION_MARKUPS,
          message: text,
          speech_rate: SpeechRates.MED,
          country: CountryCodes.IND,
          avatar_type:AvatarTypes.FULL,
          session_details:session_details,
          previous_markup:previous_markup,
        };
        await client.send(JSON.stringify(input));
    });
}

function connectToWebsocket(){
    const client=new WebSocket(ws_address);

    client.on('open',function open(){
        console.log("Connecting to the server..");
        client.on('message',function incoming_message(response){
            const parsedMessage = JSON.parse(response);
            if (parsedMessage.response_message==ResponseMessages.INITIALIZATION_COMPLETE){
                console.log("\nOutput:\n",parsedMessage);
                handle_input(client);
            }
        });
    });

    client.on('message',function incoming_message(response){
        const parsedMessage = JSON.parse(response);
        if (parsedMessage.response_message==ResponseMessages.ADD_EMOTION_MARKUPS){
            console.log("\nOutput from message: \n",parsedMessage);
            handle_input(client);
        }
    });

    client.on('error',function error(error){
        console.log("Connection error : ",error.message);
    });

    client.on('close',function close(code,reason){
        console.log("\nConnection closed with code : ",code);
        if (code==1000){
            connectToWebsocket();
        }
        else if(code==1006){
            console.log("Server Closed.");
            setTimeout(()=>{
                connectToWebsocket();
            },5000);
        }else{
            console.log("Connection closed abruptly. Trying to reconnect..")
            setTimeout(()=>{
                connectToWebsocket();
            },5000);
        }
    });
}

connectToWebsocket();