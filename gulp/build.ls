require! {
    gulp
    'gulp-less': less
    'gulp-sass': sass
    'gulp-util': gutil
    'main-bower-files': bowerfiles
    'gulp-livescript': livescript
    'gulp-browserify': browserify
}

root_path = './src'

handleError = (err) ->
    console.error err.toString!
    @emit "end"

gulp.task 'build', ['copy-js', 'copy-css', 'build-livescript', 'sass', 'browserify'] ->

gulp.task 'sass' ->
    return gulp.src "#root_path/app/scss/*.scss"
           .pipe sass!
           .pipe gulp.dest "#root_path/static/css"

gulp.task 'build-livescript' ->
    return gulp.src "#root_path/app/ls/**/*.ls"
           .pipe livescript bare: true
           .on 'error', handleError
           .pipe gulp.dest '.tmpjs'

gulp.task 'browserify', ['build-livescript'] ->
    return gulp.src '.tmpjs/coffee.js', {base: '.tmpjs'}
    .pipe browserify {insertGlobals: true, paths: ['./node_modules', './.tmpjs']}
    .on 'error', handleError
    .pipe gulp.dest "#root_path/static/js"

gulp.task 'copy-js' ->
    return gulp.src bowerfiles ['**/*.js'], {base: './vendor'}
           .pipe gulp.dest "#root_path/static/js"

gulp.task 'copy-css' ->
    return gulp.src bowerfiles ['**/*.css'], {base: './vendor'}
           .pipe gulp.dest "#root_path/static/css"

