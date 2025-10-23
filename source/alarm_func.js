exports.handler = async function(context, event, callback) {

  const notifications = true;
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

  // Data model
  const alarmType = event.alarmType;
  const alarmMessage = event.message;
  const hostName = event.values[0]['host-name'];
  const ifName = event.values[0]['if-name'] || '';
  const recipients = ['whatsapp:'+context.USER1]
  let templateName;
  let templateBody;

  // Only one alarm / one template for this demo repo
  // Template are defined in Twilio
  if (notifications && alarmType === 'intstatus') {
    templateName = context.TEMP1;
    templateBody = {
      1: alarmMessage,
      2: hostName,
      3: ifName
    }
  }

  const client = context.getTwilioClient();
  for (const user of recipients) {
    client.messages
    .create({
      from: 'whatsapp:'+context.WAPP_NUM,
      to: user,
      body: '',
      persistentAction: [],
      provideFeedback: false,
      forceDelivery: false,
      contentSid: templateName,
      contentVariables: JSON.stringify(templateBody)
    })
    .then(message => callback(null, message.sid))
    .catch(error => callback(error));
  };
};

function setUnauthorized(response) {
  response.setStatusCode(401);
  response.appendHeader("WWW-Authenticate", "Basic realm='Secure Area'");
  response.setBody("Unauthorized");

  return response;
};