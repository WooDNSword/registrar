var
    coffee     = require('gulp-coffee'),
    coffeelint = require('gulp-coffeelint'),
    gulp       = require('gulp'),
    gutil      = require('gulp-util'),
    livescript = require('gulp-livescript'),
    lslint     = require('gulp-lint-ls');

gulp.task('build', [
    'build-coffee',
    'build-coffee-tests',
    'build-livescript',
    'build-livescript-tests',
    'build-resources'
]);

gulp.task('build-coffee', function () {
    return gulp.src('./src/**/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('./dist/'));
});

gulp.task('build-coffee-tests', function () {
    return gulp.src('./test/src/**/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
	.pipe(gulp.dest('./test/dist/'));
});

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
    // Watch for CoffeeScript changes
    gulp.watch('./src/**/*.coffee', ['build-coffee']);
    // Watch for CoffeeScript test changes
    gulp.watch('./test/src/**/*.coffee', ['build-coffee-tests']);
    // Watch for LiveScript changes
    gulp.watch('./src/**/*.ls', ['build-livescript']);
    // Watch for LiveScript test changes
    gulp.watch('./test/src/**/*.ls', ['build-livescript-tests']);
    // Watch for resource changes
    gulp.watch('./src/res/**/*', ['build-resources']);
});

gulp.task('lint', [
    'lint-coffee',
    'lint-coffee-tests',
    'lint-livescript',
    'lint-livescript-tests'
]);

gulp.task('lint-coffee', function () {
    return gulp.src('./src/scripts/**/*.coffee')
        .pipe(coffeelint())
        .pipe(coffeelint.reporter());
});

gulp.task('lint-coffee-tests', function () {
    return gulp.src('./test/src/**/*.coffee')
        .pipe(coffeelint())
	.pipe(coffeelint.reporter());
});

gulp.task('lint-livescript', function () {
    return gulp.src('./src/**/*.ls')
        .pipe(lslint());
});

gulp.task('lint-livescript-tests', function () {
    return gulp.src('./test/src/**/*.ls')
        .pipe(lslint());
});

