#version 400
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec4 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

varying vec4 v_color;

void main() {
    gl_Position = projection * view * model * vec4(position,1.0);
    v_color = in_color; // Pass color to fragment shader
}
