from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import uvicorn
import asyncio
import ujson
from bili.bili_api import *  # API模块

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://www.bilibili.com",
    "Access-Control-Allow-Credentials": "true",
}


async def not_found(request, exc):
    return JSONResponse(
        {"code": -404, "message": "服务器错误，请稍后再试"}, status_code=exc.status_code
    )


async def server_error(request, exc):
    return JSONResponse(
        {"code": -500, "message": "服务器未响应,请稍后再试"}, status_code=exc.status_code
    )


exception_handlers = {404: not_found, 500: server_error}
app = Starlette(debug=True, exception_handlers=exception_handlers)


@app.route("/pgc/player/web/playurl", methods=["GET"])
async def uid(request):
    try:
        data = await pc_pgc_pcurl(request.query_params)
        return JSONResponse(ujson.loads(data), status_code=200, headers=headers)
    except Exception as err:
        print(err)
        return JSONResponse({"code": -400, "message": "服务器错误，请稍后再试"}, status_code=400)


@app.route(path="/", methods=["POST", "GET"])
async def index(request):
    return Response("By:mk39", status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=39831)
