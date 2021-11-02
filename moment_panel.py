from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from scipy.interpolate import interp2d
from matplotlib.patches import Ellipse
import matplotlib.gridspec as gs
from modules.casa_cube import casa_cube

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')


def plot_beam(ax, bmaj, bmin, bpa, color='w'):
    dx = 0.125
    dy = 0.125
    beam = Ellipse(ax.transLimits.inverted().transform((dx, dy)),
       width=bmin,
       height=bmaj,
       angle=bpa,
       fill=True,
       color=color)
    ax.add_patch(beam)

files = []
bf_files = []

vel_type = 'M9'

if vel_type == 'M9':
    files = ['../Output/S2_Final/Moment/IM_Lupi_M9.fits', '../Output/S2_Final/Moment/pseudo_casa_M9.fits']
    true_casa = [True, True]
    scale_velocity = [True, True]
    shift_velocity = [True, False]

elif vel_type == 'v0':
    files = ['../data/CASA/pseudo_casa_v0.fits', '../observations/hd_163296_CO_v0.fits']
    true_casa = [False, False]
    scale_velocity = [False, False]
    shift_velocity = [False, True]

elif vel_type == 'M1':
    files = ['../data/CASA/pseudo_casa_M1.fits', 'observations/hd_163296_CO_M1.fits']
    true_casa = [True, True]
    scale_velocity = [True, True]
    shift_velocity = [False, True]


# Fiddle with limits

# Limit in arcseconds
limit = 3.0
limit_tick = 2 * int(limit / 1.0) + 1

x_limits = [limit, -limit]
y_limits = [-limit, limit]

x_ticks = np.linspace(limit, -limit, limit_tick)
y_ticks = np.linspace(-limit, limit, limit_tick)

# Set up figure

nrows = 1
ncols = 2

print(nrows, ncols)
const = 1.8
fig = plt.figure(figsize=[const*2.5*ncols, const*2.8*nrows])

g = gs.GridSpec(
    nrows=nrows, ncols=ncols, left=0.06, bottom=0.06, right=0.88, top=0.95,
    wspace=0.08, hspace=0.02)

axes = np.array([[fig.add_subplot(g[i, j]) for i in range(0, nrows)] for j in range(0, ncols)]).T

colorbar_kwargs = {'extend': 'both', 'pad': 0.01}

pad = 0.01

bbox = dict(boxstyle="round", fc="black", alpha=0.4)
num_pixels = (2048, 2048)

colorbar_kwargs = {'extend': 'both', 'pad': pad}
plots = []

vlsr = 4500

for i in range(len(files)):
    file = files[i]
    print(file)

    moment_1_fits = fits.open(file)

    if true_casa[i]:
        data = moment_1_fits[0].data[0]
    else:
        data = moment_1_fits[0].data

    print(np.shape(data))

    if scale_velocity[i]:
        data *= 1000
    if shift_velocity[i]:
        print('scaling', i)
        data = data - vlsr

    header = moment_1_fits[0].header

    naxis1 = header['NAXIS1']
    naxis2 = header['NAXIS2']

    cdelt1 = header['CDELT1']
    cdelt2 = header['CDELT2']

    crpix1 = header['CRPIX1']
    crpix2 = header['CRPIX2']

    edge_ra = naxis1 * cdelt1 * 3600
    edge_dec = naxis2 * cdelt2 * 3600

    truemiddle_ra = edge_ra/2
    truemiddle_dec = edge_dec/2

    midpoint_ra = crpix1*cdelt1*3600
    midpoint_dec = crpix2*cdelt2*3600
    offset_ra = truemiddle_ra - midpoint_ra
    offset_dec = truemiddle_dec - midpoint_dec

    extent = np.array([-truemiddle_ra + offset_ra, truemiddle_ra + offset_ra, -truemiddle_dec + offset_dec, truemiddle_dec + offset_dec])

    h = axes[0][i].imshow(data/1000, origin='lower', cmap='RdBu_r', extent=extent, vmin=-2.0, vmax=2.0)
    axes[0][i].set_xlim(x_limits)
    axes[0][i].set_ylim(y_limits)

    plots.append(h)

titles =  ['Observation', '$5\mathrm{M_{J}}$ Model']

for i, ax in enumerate(axes[0][:]):
    ax.set_title(titles[i])


bmaj = 0.15
bmin = 0.15
bpa = 27.6
if i == 0:
    axes[0][i].set_ylabel('$\Delta$ Dec [\"]')
    plot_beam(ax, bmaj, bmin, -bpa, color=b_color[i])

cbar_labels = ['Velocity [km/s]', 'Velocity [km/s]', 'Velocity [km/s]']
b_color = ['black', 'black', 'white']


for i in range(nrows):
    for j in range(ncols):
        if j == 0:
            axes[i][j].set_ylabel('$\Delta$ Dec [\"]')
        if i == nrows-1:
            axes[i][j].set_xlabel('$\Delta$ RA [\"]')
        else:
            axes[i][j].xaxis.set_ticklabels('')

        axes[i][j].set_xticks(x_ticks)
        axes[i][j].set_yticks(y_ticks)
        if j == ncols -1:
            ax = axes[i][j]
            ax_pos = ax.get_position()
            size = 0.05
            pad = colorbar_kwargs['pad']

            width = ax_pos.width * size
            height = ax_pos.height
            bottom = ax_pos.y0 # + ax_pos.height + pad
            left = ax_pos.x0 + ax_pos.width + pad
            cax = fig.add_axes((left, bottom, width, height))
            fig.colorbar(plots[i], cax=cax, orientation='vertical', label=cbar_labels[i], **colorbar_kwargs)
            cax.xaxis.set_ticks_position('top')
            cax.xaxis.set_label_position('top')


for i in range(nrows):
    for j in range(ncols):
        axes[i][j].set_adjustable('box')
        axes[i][j].xaxis.set_ticks_position('both')
        axes[i][j].xaxis.set_tick_params(direction="in")
        axes[i][j].yaxis.set_ticks_position('both')
        axes[i][j].yaxis.set_tick_params(direction="in")
        axes[i][j].set_aspect('equal')

        if j != 0:
            axes[i][j].yaxis.set_ticklabels('')
            axes[i][j].set_ylabel('')

# plt.axis('equal')
plt.savefig('../Output/S2_Final/Moment/model_comparison_{}.pdf'.format(vel_type), dpi=300)
plt.savefig('../Output/S2_Final/Moment/model_comparison_{}.png'.format(vel_type), dpi=600)

plt.show()
