<?php
/**
 * tls-base: setup and asset loading.
 *
 * The stylesheet is design-system/base.css, the same file the static site uses, so the two
 * cannot drift apart. Each child theme adds only its brand layer: the --c-* custom properties
 * and the two typefaces.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'TLS_BASE_VERSION', '1.0.0' );

add_action( 'after_setup_theme', function () {
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'editor-styles' );
    add_editor_style( 'assets/css/base.css' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'style', 'script' ) );
} );

add_action( 'wp_enqueue_scripts', function () {
    $base = get_template_directory_uri();
    $child = get_stylesheet_directory_uri();

    // Typefaces. Self-hosting these is the next improvement: it removes a third-party request
    // and lets the Privacy Policy drop its Google Fonts section.
    $fonts = apply_filters( 'tls_google_fonts_url', '' );
    if ( $fonts ) {
        wp_enqueue_style( 'tls-fonts', $fonts, array(), null );
    }

    wp_enqueue_style( 'tls-base', $base . '/assets/css/base.css', array(), TLS_BASE_VERSION );
    if ( $child !== $base ) {
        wp_enqueue_style( 'tls-brand', $child . '/style.css', array( 'tls-base' ), TLS_BASE_VERSION );
    }
    wp_enqueue_script( 'tls-app', $base . '/assets/js/app.js', array(), TLS_BASE_VERSION, true );
} );

/**
 * Group the practice's own patterns together in the inserter, away from the core ones.
 */
add_action( 'init', function () {
    if ( function_exists( 'register_block_pattern_category' ) ) {
        register_block_pattern_category( 'tls', array( 'label' => __( 'TLS sections', 'tls-base' ) ) );
    }
} );

/**
 * Referral and sister-practice links leave the site, so they never leak which page someone
 * came from, and never hand the opened tab a reference back to this one.
 */
add_filter( 'the_content', function ( $content ) {
    return str_replace( '<a class="referral-link" href=', '<a class="referral-link" rel="noopener noreferrer" href=', $content );
} );
