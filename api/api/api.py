from datetime import datetime

import asyncio
import json
import websockets
import psutil


def output_data():
    response = dict()
    # TODO put `percpu=True`
    response["cpu"] = psutil.cpu_percent()
    response["virtualmem"] = dict()
    for attr in ["total", "available", "percent", "used", "free"]:
        response["virtualmem"][attr] = getattr(psutil.virtual_memory(), attr)
    response["swapmem"] = dict()
    for attr in ["total", "percent", "used", "free"]:
        response["swapmem"][attr] = getattr(psutil.swap_memory(), attr)
    processes = []
    for pid in psutil.pids():
        process = dict()
        try:
            p = psutil.Process(pid)
            process_exists = True
            for meth in [
                "name",
                "cmdline",
                "cpu_percent",
                "create_time",
                "exe",
                "memory_percent",
                "nice",
                "status",
                "username",
            ]:
                process[meth] = getattr(p, meth)()
            # Just some aestethic corrections:
            process["cmdline"] = " ".join(process.get("cmdline", ""))
            process["cpu_percent"] = "{:.2f}".format(
                process.get("cpu_percent", 0) * 100
            )
            process["create_time"] = datetime.fromtimestamp(
                process["create_time"]
            ).strftime("%m/%d/%Y, %H:%M:%S")
            process["memory_percent"] = "{:.2f}".format(
                process.get("memory_percent", 0) * 100
            )
            process["pid"] = pid
        except (
            FileNotFoundError,
            PermissionError,
            AttributeError,
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            process_exists = False
        if process_exists:
            processes.append(process)
    response["processes"] = processes
    return {"data": response, "command": "ping", "status": "ok", "message": ""}


def kill_process(pid):
    r = dict()
    r["command"] = "kill"
    try:
        p = psutil.Process(pid)
        p.kill()
    except (
            FileNotFoundError,
            PermissionError,
            AttributeError,
            psutil.NoSuchProcess,
            psutil.AccessDenied,
    ):
        r["status"] = "error"
    else:
        r["status"] = "ok"
    return r


async def get_request(websocket):
    async for message in websocket:
        m = json.loads(message)
        if m["command"] == "ping":
            response = output_data()
        elif m["command"] == "kill":
            response = kill_process(m["data"]["pid"])
        await websocket.send(json.dumps(response))


async def main():
    async with websockets.serve(get_request, "localhost", 3000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
