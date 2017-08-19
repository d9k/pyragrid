var gulp    = require('gulp'),
    sass    = require('gulp-ruby-sass'),
    notify  = require('gulp-notify'),
    bower   = require('gulp-bower'),
    coffee  = require('gulp-coffee'),
    gutil   = require('gulp-util'),
    babel   = require('gulp-babel'),
    rename  = require('gulp-rename'),
    sourcemaps = require('gulp-sourcemaps');

var config = {
    coffeePath: './pyragrid/resources/coffee',
    es6Path: './pyragrid/resources/es6',
    sassPath: './pyragrid/resources/sass',
//  bowerDir: './bower_components',
    nodeDir: './node_modules',
    staticDir: './pyragrid/static'
};

//gulp.task('bower', function() {
     //return bower()
         //.pipe(gulp.dest(config.bowerDir))
//}); 

gulp.task('icons', function() {
    return gulp.src(config.nodeDir + '/font-awesome/fonts/**.*')
        .pipe(gulp.dest('./public/fonts'));
});

gulp.task('css', function() {
	// thx http://stackoverflow.com/questions/28140012
    return sass(config.sassPath + '/style.sass', {
            sourcemap: true,
            //style: 'compressed',
            loadPath: [
                config.sassPath,
                config.nodeDir + '/bootstrap-sass/assets/stylesheets',
                config.nodeDir + '/font-awesome/scss'
            ]
        }).on("error", notify.onError(function (error) {
                return "Error: " + error.message;
            }))

        .pipe(sourcemaps.write(//{addComment: true, includeContent: true/*, debug: true*/}
        //TODO url prefix
        //uncomment for separate file:
        'maps', {
            includeContent: false,
            sourceRoot: 'source'
        }))
        .pipe(gulp.dest(config.staticDir + '/css'));
});

//gulp.task('coffee', function(){
    //gulp.src(config.coffeePath + '/**/*.coffee')
        //.pipe(coffee(/*{bare: true}*/).on('error', gutil.log))
        //.pipe(gulp.dest(config.staticDir + '/js'));
//});

gulp.task('es6', () => {
	gulp.src(
    config.es6Path + '/**/*.es6'
  )
	.pipe(babel({
		presets: ['es2015', 'stage-0'],
		sourceRoot: 'src',
//    sourceRoot: src.babelSourceRoot,
		sourceMap: true
	}))
	.pipe(gulp.dest(config.staticDir + '/js'));  
});

gulp.task('js-copy', function(){
    gulp.src([
            config.nodeDir + '/jquery/dist/jquery.*',
            config.nodeDir + '/jquery-ui-dist/jquery-ui.*',
            config.nodeDir + '/bootstrap-sass/assets/javascripts/bootstrap.*',
            config.nodeDir + '/datatables/media/js/jquery.dataTables.js',
            config.nodeDir + '/jqueryfiletree/dist/',
            config.nodeDir + '/lite-uploader/jquery.liteuploader*.js',
            config.nodeDir + '/blueimp-file-upload/js/jquery.fileupload.js',
            config.nodeDir + '/blueimp-file-upload/js/jquery.iframe-transport.js',
            config.nodeDir + '/blueimp-file-upload/js/vendor/jquery.ui.widget.js',
            config.nodeDir + '/blueimp-file-upload/css/jquery.fileupload.css',
            config.nodeDir + '/jinplace/js/jinplace*.js',
            config.nodeDir + '/bootstrap-confirmation2/bootstrap-confirmation*.js',
            config.nodeDir + '/nunjucks/browser/nunjucks.js',
            config.nodeDir + '/nunjucks/browser/nunjucks.min.js',
            config.nodeDir + '/mobx/lib/mobx.umd*',
            config.nodeDir + '/mobx-state-tree/dist/mobx-state-tree.umd.js',
            config.nodeDir + '/react/dist/react.*js',
            config.nodeDir + '/react-dom/dist/react-dom.*js',
            config.nodeDir + '/promise-polyfill/promise.*js',
            config.nodeDir + '/whatwg-fetch/fetch.js',            
        ]).pipe(gulp.dest(config.staticDir));

    // TODO ll bower_components/blueimp-file-upload/img

    gulp.src([
        config.nodeModules + '/tinymce/**/*'
    ]).pipe(gulp.dest(config.staticDir + '/tinymce'));

    //console.log('!' + config.bowerDir + '/jqueryfiletree/dist/connectors/**/*');

    gulp.src([
        config.nodeDir + '/jqueryfiletree/dist/**/*',
        '!' + config.nodeDir + '/jqueryfiletree/dist/connectors/**/*',
    ]).pipe(gulp.dest(config.staticDir + '/jqueryfiletree'));
    
    gulp.src(
        config.nodeDir + '/mobx-react/index*.js'
    ).pipe(rename (function (path) {
        //console.log(path);
        path.basename = path.basename.replace('index', 'mobx-react');
    })).pipe(gulp.dest(config.staticDir));
    
});


// Rerun the task when a file changes
gulp.task('watch', function() {
    //TODO try group in one array
    gulp.watch(config.sassPath + '/**/*.scss', ['css']);
    gulp.watch(config.sassPath + '/**/*.sass', ['css']);
    //gulp.watch(config.coffeePath + '/**/*.coffee', ['coffee']);
    gulp.watch(config.es6Path + '/**/*.es6', ['es6']);
 });

gulp.task('default', ['icons', 'css', 'es6', 'js-copy']);
