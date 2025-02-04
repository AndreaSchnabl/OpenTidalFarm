from dolfin import Expression  # Keep readthedocs happy

from dolfin import *
from dolfin_adjoint import *
from dolfin.cpp.log import log
# this imports NetCDFFile from netCDF4, Scientific.IO.NetCDF or scipy.io.netcdf (whichever is available)
from uptide.netcdf_reader import NetCDFFile
import utm
import uptide
import uptide.tidal_netcdf
import datetime
import scipy.interpolate
import numpy

__all__ = ["TidalForcing", "BathymetryDepthExpression"]

# We need to store tnci_time as a non-class variable, otherwise
# dolfin-adjoint tries to be clever and restores its values during the
# adjoint runs which yields an wrong behaviour for
# the "tnci_time != self.t" statement below
tnci_time = None
class TidalForcing(Expression):
    """Create a TidalForcing Expression from OTPSnc NetCDF files, where
       the grid is stored in a separate file (with "lon_z", "lat_z" and "mz"
       fields). The actual data is read from a seperate file with hRe and hIm
       fields. 

       The parameters are:

         grid_file_name
         data_file_name
         ranges
         utm_zone
         utm_band
         initial_time
         constituents
        """

    def __init__(self, **kwargs):
        self.t = 0
        self.utm_zone = kwargs["utm_zone"]
        self.utm_band = kwargs["utm_band"]

        tide = uptide.Tides(kwargs["constituents"])
        tide.set_initial_time(kwargs["initial_time"])
        self.tnci = uptide.tidal_netcdf.OTPSncTidalInterpolator(tide,
                    kwargs["grid_file_name"], kwargs["data_file_name"], kwargs["ranges"])


    def eval(self, values, X):
        """ Evaluates the tidal forcing. """
        global tnci_time
        if tnci_time != self.t:
            log(LogLevel.INFO, "Setting tidal forcing time to %f " % self.t)
            self.tnci.set_time(float(self.t))
            tnci_time = self.t

        latlon = utm.to_latlon(X[0], X[1], self.utm_zone, self.utm_band)
        try:
          # OTPS has lon, lat coordinates!
          values[0] = self.tnci.get_val((latlon[1], latlon[0]), allow_extrapolation=True)
        except uptide.netcdf_reader.CoordinateError:
          # uptide raises a CoordinateError if interpolated within the land mask, this shouldn't happen
          # but dolfin evaluates too many points in the interior of the domain which are then not used
          # but some of those might overlap with landmask, therefore set to NaN instead of raising an exception
          # so that /if/ the value is used we'll notice it
          values[0] = numpy.NaN


class BathymetryDepthExpression(Expression):
    """Create a bathymetry depth Expression from a lat/lon NetCDF file, where
       the depth values stored as "z" field. 

       Parameters are:
        filename
        utm_zone
        utm_band
        maxval. Default value is 10
        domain. Default value is None
       
       """
    def __init__(self, *args, **kwargs):

        self._domain = kwargs.get("domain", None)
        nc = NetCDFFile(kwargs["filename"], 'r')

        lat = nc.variables['lat']
        lon = nc.variables['lon']
        values = nc.variables['z']

        # work around incompatibilities in different netcdf libraries
        if hasattr(lat, 'data'): lat = lat.data
        if hasattr(lon, 'data'): lon = lon.data
        if hasattr(values, 'data'): values = values.data

        self.utm_zone = kwargs["utm_zone"]
        self.utm_band = kwargs["utm_band"]
        self.maxval = kwargs.get("maxval", 10)
        self.interpolator = scipy.interpolate.RectBivariateSpline(lat, lon, values)

    def eval(self, values, x):
        """ Evaluates the bathymetry at a point. """
        lat, lon = utm.to_latlon(x[0], x[1], self.utm_zone, self.utm_band)
        values[0] = max(self.maxval, -self.interpolator(lat, lon))
