var
    coffee = require('gulp-coffee'),
    gulp   = require('gulp'),
    gutil  = require('gulp-util');

gulp.task('build', [
    'build-coffee',
    'build-resources'
]);

gulp.task('build-coffee', function () {
    gulp.src('./src/**/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('./dist/'));
});

gulp.task('build-resources', function () {
    return gulp.src('./src/res/**/*')
        .pipe(gulp.dest('./dist/res/'));
});

gulp.task('default', function () {
    // Watch for CoffeeScript changes
    gulp.watch('./src/**/*.coffee', ['build-coffee']);
});

