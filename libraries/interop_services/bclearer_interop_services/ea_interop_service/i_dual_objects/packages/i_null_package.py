from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_package import (
    IPackage,
)


class INullPackage(IPackage):

    def __init__(self):
        IPackage.__init__(self)
        pass
