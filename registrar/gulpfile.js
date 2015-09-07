var
    coffee = require('gulp-coffee'),
    gulp   = require('gulp'),
    gutil  = require('gulp-util');

gulp.task('build-coffee', function () {
    gulp.src('./src/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('./dist/'));
});

