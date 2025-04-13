#version 400

// Recebe do programa
uniform sampler2D tex;

// Recebe da vertex shader
in vec2 v_uv;

void main(){
    vec4 texture = texture2D(tex, v_uv);
    gl_FragColor = texture;
}