from SourceCode.flask_app import create_app


if __name__ == '__main__':

    host_ip = "192.168.175.60"
    curr_app = create_app(enable_dashboard=True)
    curr_app.run(host=host_ip, port=5000, debug=True)
