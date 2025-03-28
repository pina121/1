const { createWorker } = require('@imgly/background-removal-node');

exports.handler = async function(event, context) {
    try {
        const imageData = event.body;
        const worker = await createWorker();
        const result = await worker.removeBackground(imageData);
        await worker.terminate();
        
        return {
            statusCode: 200,
            body: JSON.stringify({ result: result.toString('base64') }),
            headers: { 'Content-Type': 'application/json' }
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
