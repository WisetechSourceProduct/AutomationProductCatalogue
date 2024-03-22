THREE.ShapeUtils.triangulateShape = (function () {
    var pnlTriangulator = new PNLTRI.Triangulator();
    return function triangulateShape(contour, holes) {
    return pnlTriangulator.triangulate_polygon([contour].concat(holes));
    };
})();