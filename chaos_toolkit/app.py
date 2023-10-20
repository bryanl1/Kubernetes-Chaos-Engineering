import platform
import cherrypy
import mpi4py as MPI4 

class Root:
    @cherrypy.expose
    def index(self) -> str:
        #Simple hello world to run as service
        return "Hello Kube from {}".format(platform.node())


if __name__ == "__main__":
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080
    })
    cherrypy.quickstart(Root())

