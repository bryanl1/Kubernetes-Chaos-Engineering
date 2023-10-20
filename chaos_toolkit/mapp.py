import platform
import cherrypy
from mpi4py import MPI

#example that adds MPI
class Root:
    @cherrypy.expose
    def index(self) -> str:
        # Initialize MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        # Perform a simple computation based on the MPI rank
        if rank % 2 == 0:
            print( "Even-rank MPI process!")
        else:
            print("Odd-rank MPI process!")

        return "Hello world from {}".format(platform.node())


if __name__ == "__main__":
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080
    })
    cherrypy.quickstart(Root())

