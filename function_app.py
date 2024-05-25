import azure.functions as func
import logging
import main

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. Can deez nuts fit in yo mouth.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="timeReport", auth_level=func.AuthLevel.ANONYMOUS)
def timeReport(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function. Preparing to timereport.')

    main.main()

    return func.HttpResponse(f"Timereport successfully!")