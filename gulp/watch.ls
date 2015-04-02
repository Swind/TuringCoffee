require! {
    gulp
    'gulp-livereload': livereload
}

root_path = "./src"

gulp.task 'watch' ->
    gulp.watch "#root_path/app/ls/**/*.ls", ['build-livescript', 'browserify']
    gulp.watch "#root_path/app/scss/**/*.scss", ['sass']
