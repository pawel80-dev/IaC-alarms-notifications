exports.handler = async function(context, event, callback) {

  const response = new Twilio.Response();

  const authUser = context.MANAGER_WEBHOOK_USER;
  const authPass = context.MANAGER_WEBHOOK_PASS;
  const authHeader = event.request.headers.authorization;

  if (!authHeader) {
    return callback(null, setUnauthorized(response));
  }

  const [authType, credentials] = authHeader.split(' ');

  if (authType.toLowerCase() !== 'Basic') {
    return callback(null, setUnauthorized(response));
  }

  const [username, password] = Buffer.from(credentials, 'base64').toString().split(':');

  if (username !== authUser || password !== authPass) {
    return callback(null, setUnauthorized(response));
  }

// LATEST VERSION 1.1

//   // Set the recipient and sender numbers
//   const to = event.to || '+15558675310'; // Replace with your test number or use event input
//   const from = context.TWILIO_PHONE_NUMBER || '+15017122661'; // Set in your environment variables

//   // Set the message body
//   const body = event.body || 'Hello from Twilio Serverless Function!';

//   try {
//     // Send the SMS
//     const message = await client.messages.create({ to, from, body });
//     // Return the message SID as a response
//     return callback(null, { status: 'success', sid: message.sid });
//   } catch (error) {
//     // Return the error if sending fails
//     return callback(error);
//   }
};

function setUnauthorized(response) {
  response.setStatusCode(401);
  response.appendHeader("WWW-Authenticate", "Basic realm='Secure Area'");
  response.setBody("Unauthorized");

  return response;
};