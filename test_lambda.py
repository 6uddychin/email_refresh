const AWS = require('aws-sdk');
const csv = require('csv-parser');
const fs = require('fs');

// Initialize AWS SDK
const s3 = new AWS.S3();

exports.handler = async (event, context) => {
    try {
        // Retrieve CSV file from the source S3 bucket
        const sourceParams = {
            Bucket: 'source-bucket-name',
            Key: 'path/to/source/file.csv'
        };
        
        const csvData = await s3.getObject(sourceParams).promise();

        // Parse CSV data
        const results = [];
        const parser = csv();

        parser.on('data', (data) => {
            results.push(data);
        });

        parser.on('end', () => {
            // Extract required values from CSV data
            const account = results[0].account;
            const customerQuote1 = results[0].customer_quote1;
            const customerQuote2 = results[0].customer_quote2;
            const customerCount = results[0].customer_count;
            const customerTrend = results[0].customer_trend;
            const accountOwner = results[0].account_owner;
            const accountOwnerEmail = results[0].account_owner_email;

            // Read HTML template
            let htmlTemplate = fs.readFileSync('path/to/your/html/template.html', 'utf8');

            // Replace placeholder values in HTML template with extracted values
            htmlTemplate = htmlTemplate.replace('{Account}', account);
            htmlTemplate = htmlTemplate.replace('{customer_quote1}', customerQuote1);
            htmlTemplate = htmlTemplate.replace('{customer_quote2}', customerQuote2);
            htmlTemplate = htmlTemplate.replace('{customer_count}', customerCount);
            htmlTemplate = htmlTemplate.replace('{customer_trend}', customerTrend);
            htmlTemplate = htmlTemplate.replace('{account_owner}', accountOwner);
            htmlTemplate = htmlTemplate.replace('{account_owner_email}', accountOwnerEmail);

            // Do something with the modified HTML template, such as saving it to another S3 bucket or returning it in the response
            // For example, you can save it to another S3 bucket
            const destinationParams = {
                Bucket: 'destination-bucket-name',
                Key: 'path/to/destination/file.html',
                Body: htmlTemplate,
                ContentType: 'text/html'
            };

            s3.putObject(destinationParams, (err, data) => {
                if (err) {
                    console.error(err);
                } else {
                    console.log('HTML template updated successfully');
                }
            });
        });

        // Pipe CSV data to the parser
        fs.createReadStream(csvData.Body).pipe(parser);
    } catch (error) {
        console.error(error);
    }
};
