<?php
/**
 * LetTLSHelp: one theme, three brands.
 *
 * lettlshelp.com runs as a single WordPress install, but the root and the two practice
 * sections each have their own palette, typefaces and logo. WordPress activates one theme,
 * so the section is decided from the URL path and applied as a body class — the same
 * mechanism the static build uses.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Which section of the site is being viewed: 'life', 'leadership', or 'hub'.
 */
function tls_section() {
    $path = isset( $_SERVER['REQUEST_URI'] ) ? wp_parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ) : '/';
    $path = '/' . trim( (string) $path, '/' ) . '/';
    if ( strpos( $path, '/life-solutions/' ) === 0 ) {
        return 'life';
    }
    if ( strpos( $path, '/leadership-systems/' ) === 0 ) {
        return 'leadership';
    }
    return 'hub';
}

/**
 * The body class every brand layer in style.css is scoped to.
 */
add_filter( 'body_class', function ( $classes ) {
    $classes[] = 'site-' . tls_section();
    return $classes;
} );

/**
 * Each section loads only the typefaces it uses, rather than all three everywhere.
 */
add_filter( 'tls_google_fonts_url', function () {
    switch ( tls_section() ) {
        case 'hub':
            return 'https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Open+Sans:wght@400;600;700&family=Playfair+Display:ital@1&display=swap';
        case 'life':
            return 'https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Open+Sans:wght@400;600;700&family=Playfair+Display:ital@1&display=swap';
        case 'leadership':
            return 'https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Lato:wght@400;700&family=Playfair+Display:ital@1&display=swap';
    }
    return '';
} );
