var gulp       = require('gulp'),
    gutil      = require('gulp-util'),
    livescript = require('gulp-livescript');

gulp.task('build', [
    'build-livescript',
    'build-livescript-tests',
    'build-resources'
]);

gulp.task('build-livescript', function () {
    return gulp.src('./src/**/*.ls')
        .pipe(livescript({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('./dist/'));
});

gulp.task('build-livescript-tests', function () {
    return gulp.src('./test/src/**/*.ls')
        .pipe(livescript({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('./test/dist/'));
});

gulp.task('build-resources', function () {
    return gulp.src('./src/res/**/*')
        .pipe(gulp.dest('./dist/res/'));
});

gulp.task('default', function () {
    // Watch for LiveScript changes
    gulp.watch('./src/**/*.ls', ['build-livescript']);
    // Watch for resource changes
    gulp.watch('./src/res/**/*', ['build-resources']);
});
