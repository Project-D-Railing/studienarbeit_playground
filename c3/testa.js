
var chart = c3.generate({
    data: {
        json: {
            data3: [300, 200, 160, 400, 250, 250]
        }
    }
});

setTimeout(function () {
    chart = c3.generate({
        data: {
            json: [
                {name: 'Steinfeld', ankunft: 0, abfahrt: 2},
                {name: 'Kapsweyer', ankunft: 2, abfahrt: 2},
                {name: 'Schweighofen', ankunft: 2, abfahrt: 0},
            ],
            keys: {
                x: 'name', // it's possible to specify 'x' when category axis
                value: ['ankunft', 'abfahrt'],
            },
            type: 'bar'
        },
        axis: {
            x: {
                type: 'category'
            }
        }
    });
}, 200);