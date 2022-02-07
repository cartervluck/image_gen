# image_gen
image_gen is a package I built for generating a map for my dnd game. It has two major features, namely island generation and map drawing.

## Island Generation
To generate islands, run mapgen.py. It will create island pngs in ./imgs2. This takes a while per island.

### How it works
The algorithm can be broken up into two distinct problems, and the first problem can be broken up into three steps. For the first problem, we want to generate a low-resolution version of the map. The first step for doing so is drawing a random rectangle. Then, it removes circular chunks from the rectangle randomly. Finally, it applies a "growth formula" to the shape, randomly smoothing and growing the edges. The second problem is scaling, or turning the low res images into high res ones. The algorithm I used was a repeated bicubic interpolation (which turned out to be very slow, but functional). This works by doubling both dimensions of the matrix used to store the image, and calculating how many of the pixels in the 5x5 matrix centered on any given pixel belonged to a filled pixel in the old matrix. The threshold I set was 7, so the island grew a little and curved naturally as it interpolated. I repeated this interpolation five times.

## Map Drawing
Map drawing is a completely distinct algorithm from Island Generation, taking in a date in the fictional universe of my dnd world and changing the map to fit the given date. This is necessary because the fantasy world has rapid tectonic motion; namely, the tectonic plates are giant concentric rings that rotate relative to one another up to four times per year. Each tectonic ring is stored in its own png file.

### How it works
First we calculate how many days have passed since the "beginning of time," or the 0th day of the 1st month of the 0th year. Since each month is exactly 30 days and each year is exactly 12 months, we can calculate this with 360 * year + 30 * (month-1) + day. We want to 0-index the month so that year edges go from 360y + 30(11) + 30 to 360(y+1) + 0 + 1 (this is basically equivalent to going from 360y + 30(12) + 30 to 360(y+1) + 30(1) + 1, but year 0 is handled in a nicer way). We subtract a magic constant from the day to normalize it to what it should look like on 1-1-9999, and rotate each ring png by the rate at which they rotate times the day before pasting them onto the "background image."

### Flags

#### --timezones
Overlay timezones over the map

#### --clean
Use cleaner, less intrusive overlay visuals

#### --sun
Overlay sun's path over the map