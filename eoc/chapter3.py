from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from scene import Scene
from scene.zoomed_scene import ZoomedScene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from eoc.chapter1 import OpeningQuote, PatreonThanks
from eoc.chapter2 import DISTANCE_COLOR, TIME_COLOR, VELOCITY_COLOR
from eoc.graph_scene import *

OUTPUT_COLOR = DISTANCE_COLOR
INPUT_COLOR = TIME_COLOR
DERIVATIVE_COLOR = VELOCITY_COLOR

class Chapter3OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "You know, for a mathematician, he did not have \\\\ enough",
            "imagination.", 
            "But he has become a poet and \\\\ now he is fine.",
        ],
        "highlighted_quote_terms" : {
            "imagination." : BLUE,
        },
        "author" : "David Hilbert"
    }








class DerivativeOfXSquaredAsGraph(GraphScene, ZoomedScene, PiCreatureScene):
    CONFIG = {
        "start_x" : 2,
        "big_x" : 3,
        "dx" : 0.1,
        "x_min" : -9,
        "x_labeled_nums" : range(-8, 0, 2) + range(2, 10, 2),
        "y_labeled_nums" : range(2, 12, 2),
        "little_rect_nudge" : 0.5*(1.5*UP+RIGHT),
        "graph_origin" : 2.5*DOWN + LEFT,
        "zoomed_canvas_corner" : UP+LEFT,
    }
    def construct(self):
        self.draw_graph()
        self.ask_about_df_dx()
        self.show_differing_slopes()
        self.mention_alternate_view()

    def draw_graph(self):
        self.setup_axes()
        graph = self.get_graph(lambda x : x**2)
        label = self.get_graph_label(
            graph, "f(x) = x^2",
        )
        self.play(ShowCreation(graph))
        self.play(Write(label))
        self.dither()
        self.graph = graph

    def ask_about_df_dx(self):
        ss_group = self.get_secant_slope_group(
            self.start_x, self.graph,
            dx = self.dx,
            dx_label = "dx",
            df_label = "df",
        )
        secant_line = ss_group.secant_line
        ss_group.remove(secant_line)

        v_line, nudged_v_line = [
            self.get_vertical_line_to_graph(
                x, self.graph,
                line_class = DashedLine,
                color = RED,
                dashed_segment_length = 0.025
            )
            for x in self.start_x, self.start_x+self.dx
        ]

        df_dx = TexMobject("\\frac{df}{dx} ?")
        VGroup(*df_dx[:2]).highlight(ss_group.df_line.get_color())
        VGroup(*df_dx[3:5]).highlight(ss_group.dx_line.get_color())
        df_dx.next_to(
            self.input_to_graph_point(self.start_x, self.graph),
            DOWN+RIGHT,
            buff = MED_SMALL_BUFF
        )

        self.play(ShowCreation(v_line))
        self.dither()
        self.play(Transform(v_line.copy(), nudged_v_line))
        self.remove(self.get_mobjects_from_last_animation()[0])
        self.add(nudged_v_line)
        self.dither()
        self.activate_zooming()
        self.little_rectangle.replace(self.big_rectangle)
        self.play(
            FadeIn(self.little_rectangle),
            FadeIn(self.big_rectangle),
        )
        self.play(
            ApplyFunction(
                lambda r : self.position_little_rectangle(r, ss_group),
                self.little_rectangle
            ),
            self.pi_creature.change_mode, "pondering",
            self.pi_creature.look_at, ss_group
        )
        self.play(
            ShowCreation(ss_group.dx_line),
            Write(ss_group.dx_label),
        )
        self.dither()
        self.play(
            ShowCreation(ss_group.df_line),
            Write(ss_group.df_label),
        )
        self.dither()
        self.play(Write(df_dx))
        self.dither()
        self.play(*map(FadeOut, [
            v_line, nudged_v_line,
        ]))
        self.ss_group = ss_group

    def position_little_rectangle(self, rect, ss_group):
        rect.scale_to_fit_width(3*self.dx)
        rect.move_to(
            ss_group.dx_line.get_left()
        )
        rect.shift(
            self.dx*self.little_rect_nudge
        )
        return rect

    def show_differing_slopes(self):
        ss_group = self.ss_group
        def rect_update(rect):
            self.position_little_rectangle(rect, ss_group)

        self.play(
            ShowCreation(ss_group.secant_line),
            self.pi_creature.change_mode, "thinking"
        )
        ss_group.add(ss_group.secant_line)
        self.dither()
        for target_x in self.big_x, -self.dx/2, 1, 2:
            self.animate_secant_slope_group_change(
                ss_group, target_x = target_x,
                added_anims = [
                    UpdateFromFunc(self.little_rectangle, rect_update)
                ]
            )
            self.dither()

    def mention_alternate_view(self):
        self.remove(self.pi_creature)
        everything = VGroup(*self.get_mobjects())
        self.add(self.pi_creature)
        self.disactivate_zooming()
        self.play(
            ApplyMethod(
                everything.shift, 2*SPACE_WIDTH*LEFT,
                rate_func = lambda t : running_start(t, -0.1)
            ),
            self.pi_creature.change_mode, "happy"
        )
        self.say("Let's try \\\\ another view.", target_mode = "speaking")
        self.dither(2)

class NudgeSideLengthOfSquare(PiCreatureScene):
    CONFIG = {
        "square_width" : 3,
        "alt_square_width" : 5,
        "dx" : 0.25,
        "alt_dx" : 0.01,
        "square_color" : GREEN,
        "square_fill_opacity" : 0.75,
        "three_color" : GREEN,
        "dx_color" : BLUE_B,
        "is_recursing_on_dx" : False,
        "is_recursing_on_square_width" : False,
    }
    def construct(self):
        ApplyMethod(self.pi_creature.change_mode, "speaking").update(1)
        self.add_function_label()
        self.introduce_square()
        self.increase_area()
        self.write_df_equation()
        self.highlight_shapes()
        self.examine_thin_rectangles()
        self.examine_tiny_square()
        self.show_smaller_dx()
        self.rule_of_thumb()
        self.write_out_derivative()

    def add_function_label(self):
        label = TexMobject("f(x) = x^2")
        label.next_to(ORIGIN, RIGHT, buff = (self.square_width-3)/2.)
        label.to_edge(UP)
        self.add(label)
        self.function_label = label

    def introduce_square(self):
        square = Square(
            side_length = self.square_width,
            stroke_width = 0,
            fill_opacity = self.square_fill_opacity,
            fill_color = self.square_color,
        )
        square.to_corner(UP+LEFT, buff = LARGE_BUFF)
        x_squared = TexMobject("x^2")
        x_squared.move_to(square)

        braces = VGroup()
        for vect in RIGHT, DOWN:
            brace = Brace(square, vect)
            text = brace.get_text("$x$")
            brace.add(text)
            braces.add(brace)

        self.play(
            DrawBorderThenFill(square),
            self.pi_creature.change_mode, "plain"
        )
        self.play(*map(GrowFromCenter, braces))
        self.play(Write(x_squared))
        self.change_mode("pondering")
        self.dither()

        self.square = square
        self.side_braces = braces

    def increase_area(self):
        color_kwargs = {
            "fill_color" : YELLOW,
            "fill_opacity" : self.square_fill_opacity,
            "stroke_width" : 0,
        }
        right_rect = Rectangle(
            width = self.dx,
            height = self.square_width,
            **color_kwargs
        )
        bottom_rect = right_rect.copy().rotate(-np.pi/2)
        right_rect.next_to(self.square, RIGHT, buff = 0)
        bottom_rect.next_to(self.square, DOWN, buff = 0)
        corner_square = Square(
            side_length = self.dx,
            **color_kwargs
        )
        corner_square.next_to(self.square, DOWN+RIGHT, buff = 0)

        right_line = Line(
            self.square.get_corner(UP+RIGHT),
            self.square.get_corner(DOWN+RIGHT),
            stroke_width = 0
        )
        bottom_line = Line(
            self.square.get_corner(DOWN+RIGHT),
            self.square.get_corner(DOWN+LEFT),
            stroke_width = 0
        )
        corner_point = VectorizedPoint(
            self.square.get_corner(DOWN+RIGHT)
        )

        little_braces = VGroup()
        for vect in RIGHT, DOWN:
            brace = Brace(
                corner_square, vect, 
                buff = SMALL_BUFF,
                tex_string = "\\underbrace{%s}"%(3*"\\quad"),
            )
            text = brace.get_text("$dx$", buff = SMALL_BUFF)
            text.highlight(self.dx_color)
            brace.add(text)
            little_braces.add(brace)

        right_brace, bottom_brace = self.side_braces
        self.play(
            Transform(right_line, right_rect),
            Transform(bottom_line, bottom_rect),
            Transform(corner_point, corner_square),
            right_brace.next_to, right_rect, RIGHT, SMALL_BUFF,
            bottom_brace.next_to, bottom_rect, DOWN, SMALL_BUFF,
        )
        self.remove(corner_point, bottom_line, right_line)
        self.add(corner_square, bottom_rect, right_rect)
        self.play(*map(GrowFromCenter, little_braces))
        self.dither()
        self.play(*it.chain(*[
            [mob.shift, vect*SMALL_BUFF]
            for mob, vect in [
                (right_rect, RIGHT),
                (bottom_rect, DOWN),
                (corner_square, DOWN+RIGHT),
                (right_brace, RIGHT),
                (bottom_brace, DOWN),
                (little_braces, DOWN+RIGHT)
            ]
        ]))
        self.change_mode("thinking")
        self.dither()
        self.right_rect = right_rect
        self.bottom_rect = bottom_rect
        self.corner_square = corner_square
        self.little_braces = little_braces

    def write_df_equation(self):
        right_rect = self.right_rect
        bottom_rect = self.bottom_rect
        corner_square = self.corner_square

        df_equation = VGroup(
            TexMobject("df").highlight(right_rect.get_color()),
            TexMobject("="),
            right_rect.copy(),
            TextMobject("+"),
            right_rect.copy(),
            TexMobject("+"),
            corner_square.copy()
        )
        df_equation.arrange_submobjects()
        df_equation.next_to(
            self.function_label, DOWN, 
            aligned_edge = LEFT,
            buff = SMALL_BUFF
        )
        df, equals, r1, plus1, r2, plus2, s = df_equation

        pairs = [
            (df, self.function_label[0]),
            (r1, right_rect), 
            (r2, bottom_rect), 
            (s, corner_square),
        ]
        for mover, origin in pairs:
            mover.save_state()
            Transform(mover, origin).update(1)
        self.play(df.restore)
        self.dither()
        self.play(
            *[
                mob.restore
                for mob in r1, r2, s
            ]+[
                Write(symbol)
                for symbol in equals, plus1, plus2
            ], 
            run_time = 2
        )
        self.change_mode("happy")
        self.dither()

        self.df_equation = df_equation

    def highlight_shapes(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation

        tups = [
            (self.right_rect, self.bottom_rect, r1, r2),
            (self.corner_square, s)
        ]
        for tup in tups:
            self.play(
                *it.chain(*[
                    [m.scale_in_place, 1.2, m.highlight, RED]
                    for m in tup
                ]), 
                rate_func = there_and_back
            )
            self.dither()

    def examine_thin_rectangles(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation

        rects = VGroup(r1, r2)
        thin_rect_brace = Brace(rects, DOWN)
        text = thin_rect_brace.get_text("$2x \\, dx$")
        VGroup(*text[-2:]).highlight(self.dx_color)
        text.save_state()
        alt_text = thin_rect_brace.get_text("$2(3)(0.01)$")
        alt_text[2].highlight(self.three_color)
        VGroup(*alt_text[-5:-1]).highlight(self.dx_color)

        example_value = TexMobject("=0.06")
        example_value.next_to(alt_text, DOWN)

        self.play(GrowFromCenter(thin_rect_brace))
        self.play(
            Write(text),
            self.pi_creature.change_mode, "pondering"
        )
        self.dither()

        xs = VGroup(*[
            brace[-1] 
            for brace in self.side_braces
        ])
        dxs = VGroup(*[
            brace[-1]
            for brace in self.little_braces
        ])
        for group, tex, color in (xs, "3", self.three_color), (dxs, "0.01", self.dx_color):
            group.save_state()            
            group.generate_target()            
            for submob in group.target:
                number = TexMobject(tex)
                number.highlight(color)
                number.move_to(submob, LEFT)
                Transform(submob, number).update(1)
        self.play(MoveToTarget(xs))
        self.play(MoveToTarget(dxs))
        self.dither()
        self.play(Transform(text, alt_text))
        self.dither()
        self.play(Write(example_value))
        self.dither()
        self.play(
            FadeOut(example_value),
            *[
                mob.restore
                for mob in xs, dxs, text
            ]
        )
        self.remove(text)
        text.restore()
        self.add(text)

        self.dither()
        self.dxs = dxs
        self.thin_rect_brace = thin_rect_brace
        self.thin_rect_area = text        

    def examine_tiny_square(self):
        text = TexMobject("dx^2")
        VGroup(*text[:2]).highlight(self.dx_color)
        text.next_to(self.df_equation[-1], UP)
        text.save_state()
        alt_text = TextMobject("0.0001")
        alt_text.move_to(text)

        self.play(Write(text))
        self.change_mode("surprised")
        self.dither()
        self.play(
            MoveToTarget(self.dxs),
            self.pi_creature.change_mode, "plain"
        )
        for submob in self.dxs.target:
            number = TexMobject("0.01")
            number.highlight(self.dx_color)
            number.move_to(submob, LEFT)
            Transform(submob, number).update(1)
        self.play(MoveToTarget(self.dxs))
        self.play(
            Transform(text, alt_text),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.dither(2)
        self.play(*[
            mob.restore
            for mob in self.dxs, text
        ] + [
            self.pi_creature.change_mode, "erm"
        ])
        self.dx_squared = text

    def show_smaller_dx(self):
        self.mobjects_at_start_of_show_smaller_dx = [
            mob.copy() for mob in self.get_mobjects()
        ]
        if self.is_recursing_on_dx:
            return

        alt_scene = self.__class__(
            skip_animations = True,
            dx = self.alt_dx,
            is_recursing_on_dx = True
        )
        for mob in self.get_mobjects():
            mob.save_state()
        self.play(*[
            Transform(*pair)
            for pair in zip(
                self.get_mobjects(),
                alt_scene.mobjects_at_start_of_show_smaller_dx,
            )
        ])
        self.dither()
        self.play(*[
            mob.restore
            for mob in self.get_mobjects()
        ])
        self.change_mode("happy")
        self.dither()

    def rule_of_thumb(self):
        circle = Circle(color = RED)
        dx_squared_group = VGroup(self.dx_squared, self.df_equation[-1])
        circle.replace(dx_squared_group, stretch = True)
        dx_squared_group.add(self.df_equation[-2])
        circle.scale_in_place(1.5)
        safe_to_ignore = TextMobject("Safe to ignore")
        safe_to_ignore.next_to(circle, DOWN, aligned_edge = LEFT)
        safe_to_ignore.highlight(circle.get_color())

        self.play(ShowCreation(circle))
        self.play(
            Write(safe_to_ignore, run_time = 2),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.play(
            FadeOut(circle),
            FadeOut(safe_to_ignore),
            dx_squared_group.fade, 0.5,
            dx_squared_group.to_corner, UP+RIGHT,
            self.pi_creature.change_mode, "plain"
        )
        self.dither()

    def write_out_derivative(self):
        df, equals, r1, plus1, r2, plus2, s = self.df_equation
        frac_line = TexMobject("-")
        frac_line.stretch_to_fit_width(df.get_width())
        frac_line.move_to(df)
        dx = VGroup(*self.thin_rect_area[-2:]) 
        x = self.thin_rect_area[1]

        self.play(
            Transform(r1, self.right_rect),
            Transform(r2, self.bottom_rect),
            FadeOut(plus1),
            FadeOut(self.thin_rect_brace)
        )
        self.play(
            self.thin_rect_area.next_to, VGroup(df, equals),
            RIGHT, MED_SMALL_BUFF, UP,
            self.pi_creature.change_mode, "thinking"
        )
        self.dither(2)
        self.play(
            ApplyMethod(df.next_to, frac_line, UP, SMALL_BUFF),
            ApplyMethod(dx.next_to, frac_line, DOWN, SMALL_BUFF),
            Write(frac_line),            
            path_arc = -np.pi
        )
        self.dither()

        brace_xs = [
            brace[-1]
            for brace in self.side_braces
        ]
        xs = list(brace_xs) + [x]
        for x_mob in xs:
            number = TexMobject("(%d)"%self.square_width)
            number.move_to(x_mob, LEFT)
            number.shift(
                (x_mob.get_bottom()[1] - number[1].get_bottom()[1])*UP
            )
            x_mob.save_state()
            x_mob.target = number
        self.play(*map(MoveToTarget, xs))
        self.dither(2)

        #Recursively transform to what would have happened
        #with a wider square width
        self.mobjects_at_end_of_write_out_derivative = self.get_mobjects()
        if self.is_recursing_on_square_width or self.is_recursing_on_dx:
            return
        alt_scene = self.__class__(
            skip_animations = True,
            square_width = self.alt_square_width,
            is_recursing_on_square_width = True,
        )
        self.play(*[
            Transform(*pair)
            for pair in zip(
                self.mobjects_at_end_of_write_out_derivative,
                alt_scene.mobjects_at_end_of_write_out_derivative
            )
        ])
        self.change_mode("happy")
        self.dither(2)

class NudgeSideLengthOfCube(Scene):
    CONFIG = {
        "x_color" : BLUE,
        "dx_color" : GREEN,
        "df_color" : YELLOW,
        "use_morty" : False,
        "x" : 3,
        "dx" : 0.2,
        "alt_dx" : 0.02,
        "offset_vect" : OUT,
        "pose_angle" : np.pi/12,
        "pose_axis" : UP+RIGHT,
        "small_piece_scaling_factor" : 0.7,
        "allow_recursion" : True,
    }
    def construct(self):
        self.states = dict()
        if self.allow_recursion:
            self.alt_scene = self.__class__(
                skip_animations = True,
                allow_recursion = False,
                dx = self.alt_dx,
            )

        self.add_title()
        self.introduce_cube()
        self.write_df_equation()
        self.write_derivative()

    def add_title(self):
        title = TexMobject("f(x) = x^3")
        title.shift(SPACE_WIDTH*LEFT/2)
        title.to_edge(UP)
        self.play(Write(title))
        self.dither()

    def introduce_cube(self):
        cube = self.get_cube()
        cube.to_edge(LEFT, buff = 2*LARGE_BUFF)
        cube.shift(DOWN)

        dv_pieces = self.get_dv_pices(cube)
        original_dx = self.dx
        self.dx = 0
        alt_dv_pieces = self.get_dv_pices(cube)
        self.dx = original_dx
        alt_dv_pieces.set_fill(opacity = 0)

        x_brace = Brace(cube, LEFT, buff = SMALL_BUFF)
        dx_brace = Brace(
            dv_pieces[1], LEFT, buff = SMALL_BUFF,
            tex_string = "\\underbrace{%s}"%(3*"\\quad"),
        )
        dx_brace.stretch_in_place(1.5, 1)
        for brace, tex in (x_brace, "x"), (dx_brace, "dx"):
            brace.scale_in_place(0.95)
            brace.rotate_in_place(-np.pi/96)
            brace.shift(0.3*(UP+LEFT))
            brace.add(brace.get_text("$%s$"%tex))


        cube_group = VGroup(cube, dv_pieces, alt_dv_pieces)
        self.pose_3d_mobject(cube_group)

        self.play(DrawBorderThenFill(cube))
        self.play(GrowFromCenter(x_brace))
        self.dither()
        self.play(Transform(alt_dv_pieces, dv_pieces))
        self.remove(alt_dv_pieces)
        self.add(dv_pieces)
        self.play(GrowFromCenter(dx_brace))
        self.dither()
        for piece in dv_pieces:
            piece.on_cube_state = piece.copy()
        self.play(*[
            ApplyMethod(
                piece.shift, 
                0.5*(piece.get_center()-cube.get_center())
            )
            for piece in dv_pieces
        ]+[
            ApplyMethod(dx_brace.shift, 0.7*UP)
        ])
        self.dither()

        self.cube = cube
        self.dx_brace = dx_brace
        self.faces, self.bars, self.corner_cube = [
            VGroup(*[
                piece 
                for piece in dv_pieces
                if piece.type == target_type
            ])
            for target_type in "face", "bar", "corner_cube"
        ]

    def write_df_equation(self):
        df_equation = VGroup(
            TexMobject("df"),
            TexMobject("="),
            self.organize_faces(self.faces.copy()),
            TexMobject("+"),
            self.organize_bars(self.bars.copy()),
            TexMobject("+"),
            self.corner_cube.copy()
        )
        df, equals, faces, plus1, bars, plus2, corner_cube = df_equation
        df.highlight(self.df_color)
        for three_d_mob in faces, bars, corner_cube:
            three_d_mob.scale(self.small_piece_scaling_factor)
            # self.pose_3d_mobject(three_d_mob)
        faces.set_fill(opacity = 0.3)
        df_equation.arrange_submobjects(RIGHT)
        df_equation.next_to(ORIGIN, RIGHT)
        df_equation.to_edge(UP)

        faces_brace = Brace(faces, DOWN)
        derivative = faces_brace.get_text("$3x^2", "\\, dx$")
        extras_brace = Brace(VGroup(bars, corner_cube), DOWN)
        ignore_text = extras_brace.get_text(
            "Multiple \\\\ of $dx^2$"
        )
        ignore_text.scale_in_place(0.7)
        x_squared_dx = TexMobject("x^2", "\\, dx")


        self.play(*map(Write, [df, equals]))
        self.grab_pieces(self.faces, faces)
        self.dither()
        self.shrink_dx("Faces are introduced")
        face = self.faces[0]
        face.save_state()
        self.play(face.shift, SPACE_WIDTH*RIGHT)
        x_squared_dx.next_to(face, LEFT)
        self.play(Write(x_squared_dx, run_time = 1))
        self.dither()
        for submob, sides in zip(x_squared_dx, [face[0], VGroup(*face[1:])]):
            self.play(
                submob.highlight, RED,
                sides.highlight, RED,
                rate_func = there_and_back
            )
            self.dither()
        self.play(
            face.restore,
            Transform(
                x_squared_dx, derivative,
                replace_mobject_with_target_in_scene = True
            ),
            GrowFromCenter(faces_brace)
        )
        self.dither()
        self.grab_pieces(self.bars, bars, plus1)
        self.grab_pieces(self.corner_cube, corner_cube, plus2)
        self.play(
            GrowFromCenter(extras_brace),
            Write(ignore_text)
        )
        self.dither()
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in [
                plus1, bars, plus2, corner_cube, 
                extras_brace, ignore_text
            ]
        ])
        self.dither()

        self.df_equation = df_equation
        self.derivative = derivative

    def write_derivative(self):
        df, equals, faces, plus1, bars, plus2, corner_cube = self.df_equation
        df = df.copy()
        equals = equals.copy()        
        df_equals = VGroup(df, equals)        

        derivative = self.derivative.copy()
        dx = derivative[1]

        extra_stuff = TexMobject("+(\\dots)", "dx^2")
        dx_squared = extra_stuff[1]

        derivative.generate_target()
        derivative.target.shift(2*DOWN)
        extra_stuff.next_to(derivative.target)
        self.play(
            MoveToTarget(derivative),
            df_equals.next_to, derivative.target[0], LEFT,
            df_equals.shift, 0.07*DOWN
        )
        self.play(Write(extra_stuff))
        self.dither()

        frac_line = TexMobject("-")
        frac_line.replace(df)
        extra_stuff.generate_target()
        extra_stuff.target.next_to(derivative[0])
        frac_line2 = TexMobject("-")
        frac_line2.stretch_to_fit_width(
            extra_stuff.target[1].get_width()
        )
        frac_line2.move_to(extra_stuff.target[1])
        extra_stuff.target[1].next_to(frac_line2, UP, buff = SMALL_BUFF)
        dx_below_dx_squared = TexMobject("dx")
        dx_below_dx_squared.next_to(frac_line2, DOWN, buff = SMALL_BUFF)
        self.play(
            FadeIn(frac_line),
            FadeIn(frac_line2),
            df.next_to, frac_line, UP, SMALL_BUFF,
            dx.next_to, frac_line, DOWN, SMALL_BUFF,
            MoveToTarget(extra_stuff),
            Write(dx_below_dx_squared),
            path_arc = -np.pi
        )
        self.dither()
        inner_dx = VGroup(*dx_squared[:-1])
        self.play(
            FadeOut(frac_line2),
            FadeOut(dx_below_dx_squared),
            dx_squared[-1].highlight, BLACK,
            inner_dx.next_to, extra_stuff[0], RIGHT, SMALL_BUFF
        )
        self.dither()
        self.shrink_dx("Derivative is written", restore = False)
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in extra_stuff, inner_dx
        ])
        self.dither(2)

        anims = []
        for mob in list(self.faces)+list(self.bars)+list(self.corner_cube):
            vect = mob.get_center()-self.cube.get_center()
            anims += [
                mob.shift, -(1./3)*vect
            ]
        anims += self.dx_brace.shift, 0.7*DOWN
        self.play(*anims)
        self.dither()

    def grab_pieces(self, start_pieces, end_pices, to_write = None):
        for piece in start_pieces:
            piece.generate_target()
            piece.target.rotate_in_place(
                np.pi/12, piece.get_center()-self.cube.get_center()
            )
            piece.target.highlight(RED)
        self.play(*map(MoveToTarget, start_pieces), rate_func = wiggle)
        self.dither()
        added_anims = []
        if to_write is not None:
            added_anims.append(Write(to_write))
        self.play(
            Transform(start_pieces.copy(), end_pices),
            *added_anims
        )

    def shrink_dx(self, state_name, restore = True):
        mobjects = self.get_mobjects()
        mobjects_with_points = [
            m for m in mobjects
            if m.get_num_points() > 0
        ]
        #Alt_scene will reach this point, and save copy of self
        #in states dict
        self.states[state_name] = [
            mob.copy() for mob in mobjects_with_points
        ] 
        if not self.allow_recursion:
            return
        if restore:
            movers = self.states[state_name]
            for mob in movers:
                mob.save_state()
            self.remove(*mobjects)
        else:
            movers = mobjects_with_points
        self.play(*[
            Transform(*pair)
            for pair in zip(
                movers,
                self.alt_scene.states[state_name]
            )
        ])
        self.dither()
        if restore:
            self.play(*[m.restore for m in movers])
            self.remove(*movers)
            self.mobjects = mobjects

    def get_cube(self):
        cube = self.get_prism(self.x, self.x, self.x)
        cube.set_fill(color = BLUE, opacity = 0.3)
        cube.set_stroke(color = WHITE, width = 1)
        return cube

    def get_dv_pices(self, cube):
        pieces = VGroup()
        for vect in it.product([0, 1], [0, 1], [0, 1]):
            if np.all(vect == ORIGIN):
                continue
            args = [
                self.x if bit is 0 else self.dx
                for bit in vect
            ]
            piece = self.get_prism(*args)
            piece.next_to(cube, np.array(vect), buff = 0)
            pieces.add(piece)
            if sum(vect) == 1:
                piece.type = "face"
            elif sum(vect) == 2:
                piece.type = "bar"
            else:
                piece.type = "corner_cube"

        return pieces

    def organize_faces(self, faces):
        self.unpose_3d_mobject(faces)
        for face in faces:
            dimensions = [
                face.length_over_dim(dim)
                for dim in range(3)
            ]
            thin_dim = np.argmin(dimensions)
            if thin_dim == 0:
                face.rotate(np.pi/2, DOWN)
            elif thin_dim == 1:
                face.rotate(np.pi/2, RIGHT)
        faces.arrange_submobjects(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(faces)
        return faces

    def organize_bars(self, bars):
        self.unpose_3d_mobject(bars)
        for bar in bars:
            dimensions = [
                bar.length_over_dim(dim)
                for dim in range(3)
            ]
            thick_dim = np.argmax(dimensions)
            if thick_dim == 0:
                bar.rotate(np.pi/2, OUT)
            elif thick_dim == 2:
                bar.rotate(np.pi/2, LEFT)
        bars.arrange_submobjects(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(bars)
        return bars

    def get_corner_cube(self):
        return self.get_prism(self.dx, self.dx,  self.dx)


    def get_prism(self, width, height, depth):
        color_kwargs = {
            "fill_color" : YELLOW,
            "fill_opacity" : 0.4,
            "stroke_color" : WHITE,            
            "stroke_width" : 0.1,
        }
        front = Rectangle(
            width = width,
            height = height,
            **color_kwargs
        )
        face = VGroup(front)
        for vect in LEFT, RIGHT, UP, DOWN:
            if vect is LEFT or vect is RIGHT:
                side = Rectangle(
                    height = height, 
                    width = depth, 
                    **color_kwargs
                )
            else:
                side = Rectangle(
                    height = depth,
                    width = width, 
                    **color_kwargs
                )
            side.next_to(front, vect, buff = 0)
            side.rotate(
                np.pi/2, rotate_vector(vect, -np.pi/2),
                about_point = front.get_edge_center(vect)
            )
            face.add(side)
        return face

    def pose_3d_mobject(self, mobject):
        mobject.rotate_in_place(self.pose_angle, self.pose_axis)
        return mobject

    def unpose_3d_mobject(self, mobject):
        mobject.rotate_in_place(-self.pose_angle, self.pose_axis)
        return mobject

class ShowCubeDVIn3D(Scene):
    def construct(self):
        raise Exception("This scene is only here for the stage_scenes script.")

class GraphOfXCubed(GraphScene):
    CONFIG = {
        "x_min" : -6,
        "x_max" : 6,
        "x_axis_width" : 2*SPACE_WIDTH,
        "x_labeled_nums" : range(-6, 7),
        "y_min" : -35,
        "y_max" : 35,
        "y_axis_height" : 2*SPACE_HEIGHT,
        "y_tick_frequency" : 5,
        "y_labeled_nums" : range(-30, 40, 10),
        "graph_origin" : ORIGIN,
        "dx" : 0.2,
        "deriv_x_min" : -3,
        "deriv_x_max" : 3,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.get_graph(lambda x : x**3)
        label = self.get_graph_label(
            graph, "f(x) = x^3",
            direction = LEFT,
        )


        deriv_graph, full_deriv_graph = [
            self.get_derivative_graph(
                graph,
                color = DERIVATIVE_COLOR,
                x_min = low_x,
                x_max = high_x,
            )
            for low_x, high_x in [
                (self.deriv_x_min, self.deriv_x_max),
                (self.x_min, self.x_max),
            ]
        ]
        deriv_label = self.get_graph_label(
            deriv_graph,
            "\\frac{df}{dx}(x) = 3x^2",
            x_val = -3, 
            direction = LEFT
        )
        deriv_label.shift(0.5*DOWN)

        ss_group = self.get_secant_slope_group(
            self.deriv_x_min, graph, 
            dx = self.dx,
            dx_line_color = WHITE,
            df_line_color = WHITE,
            secant_line_color = YELLOW,
        )

        self.play(ShowCreation(graph))
        self.play(Write(label, run_time = 1))
        self.dither()
        self.play(Write(deriv_label, run_time = 1))
        self.play(ShowCreation(ss_group, submobject_mode = "all_at_once"))
        self.animate_secant_slope_group_change(
            ss_group,
            target_x = self.deriv_x_max,
            run_time = 10,
            added_anims = [
                ShowCreation(deriv_graph, run_time = 10)
            ]
        )
        self.play(FadeIn(full_deriv_graph))
        self.dither()
        for x_val in -2, -self.dx/2, 2:
            self.animate_secant_slope_group_change(
                ss_group,
                target_x = x_val,
                run_time = 2
            )
            if x_val != -self.dx/2:
                v_line = self.get_vertical_line_to_graph(
                    x_val, deriv_graph,
                    line_class = DashedLine
                )
                self.play(ShowCreation(v_line))
                self.play(FadeOut(v_line))

class PatternForPowerRule(PiCreatureScene):
    CONFIG = {
        "num_exponents" : 5,
    }
    def construct(self):
        self.introduce_pattern()
        self.generalize_pattern()
        self.show_hopping()

    def introduce_pattern(self):
        exp_range = range(1, 1+self.num_exponents)
        colors = color_gradient([BLUE_D, YELLOW], self.num_exponents)
        derivatives = VGroup()
        for exponent, color in zip(exp_range, colors):
            derivative = TexMobject(
                "\\frac{d(x^%d)}{dx} = "%exponent,
                "%d x^{%d}"%(exponent, exponent-1)
            )
            VGroup(*derivative[0][2:4]).highlight(color)
            derivatives.add(derivative)
        derivatives.arrange_submobjects(
            DOWN, aligned_edge = LEFT,
            buff = MED_LARGE_BUFF
        )
        derivatives.scale_to_fit_height(2*SPACE_HEIGHT-1)
        derivatives.to_edge(LEFT)

        self.play(FadeIn(derivatives[0]))
        for d1, d2 in zip(derivatives, derivatives[1:]):
            self.play(Transform(
                d1.copy(), d2,
                replace_mobject_with_target_in_scene = True  
            ))
        self.change_mode("thinking")
        self.dither()
        for derivative in derivatives[-2:]:
            derivative.save_state()
            self.play(
                derivative.scale, 2,
                derivative.next_to, derivative,
                RIGHT, SMALL_BUFF, DOWN,
            )
            self.dither(2)
            self.play(derivative.restore)
            self.remove(derivative)
            derivative.restore()
            self.add(derivative)

        self.derivatives = derivatives
        self.colors = colors

    def generalize_pattern(self):
        derivatives = self.derivatives


        power_rule = TexMobject(
            "\\frac{d (x^n)}{dx} = ",
            "nx^{n-1}"
        )
        title = TextMobject("``Power rule''")        
        title.next_to(power_rule, UP, MED_LARGE_BUFF)
        lines = VGroup(*[
            Line(
                deriv.get_right(), power_rule.get_left(),
                buff = MED_SMALL_BUFF,
                color = deriv[0][2].get_color()
            )
            for deriv in derivatives
        ])

        self.play(
            Transform(
                VGroup(*[d[0].copy() for d in derivatives]),
                VGroup(power_rule[0]),
                replace_mobject_with_target_in_scene = True
            ),
            ShowCreation(lines),
            submobject_mode = "lagged_start",
            run_time = 2,
        )
        self.dither()
        self.play(Write(power_rule[1]))
        self.dither()
        self.play(
            Write(title),
            self.pi_creature.change_mode, "speaking"
        )
        self.dither()

    def show_hopping(self):
        exp_range = range(2, 2+self.num_exponents-1)
        self.change_mode("tired")
        for exp, color in zip(exp_range, self.colors[1:]):
            form = TexMobject(
                "x^",
                str(exp),
                "\\rightarrow",
                str(exp),
                "x^",
                str(exp-1)
            )
            form.highlight(color)
            form.to_corner(UP+RIGHT, buff = LARGE_BUFF)
            lhs = VGroup(*form[:2])
            lhs_copy = lhs.copy()
            rhs = VGroup(*form[-2:])
            arrow = form[2]

            self.play(Write(lhs))
            self.play(
                lhs_copy.move_to, rhs, DOWN+LEFT,
                Write(arrow)
            )
            self.dither()
            self.play(
                ApplyMethod(
                    lhs_copy[1].replace, form[3],
                    path_arc = np.pi,
                    rate_func = running_start,
                ),
                FadeIn(
                    form[5],
                    rate_func = squish_rate_func(smooth, 0.5, 1)
                )   
            )
            self.dither()
            self.play(
                self.pi_creature.change_mode, "hesitant",
                self.pi_creature.look_at, lhs_copy
            )
            self.play(*map(FadeOut, [form, lhs_copy]))

class PowerRuleAlgebra(Scene):
    CONFIG = {
        "dx_color" : YELLOW,
        "x_color" : BLUE,
    }
    def construct(self):
        x_to_n = TexMobject("x^n")
        down_arrow = Arrow(UP, DOWN, buff = MED_LARGE_BUFF)
        paren_strings = ["(", "x", "+", "dx", ")"]
        x_dx_to_n = TexMobject(*paren_strings +["^n"])
        equals = TexMobject("=")
        equals2 = TexMobject("=")
        full_product = TexMobject(
            *paren_strings*3+["\\cdots"]+paren_strings
        )

        x_to_n.highlight(self.x_color)
        for mob in x_dx_to_n, full_product:
            mob.highlight_by_tex("dx", self.dx_color)
            mob.highlight_by_tex("x", self.x_color)

        nudge_group = VGroup(x_to_n, down_arrow, x_dx_to_n)
        nudge_group.arrange_submobjects(DOWN)
        nudge_group.to_corner(UP+LEFT)
        down_arrow.next_to(x_to_n[0], DOWN)
        equals.next_to(x_dx_to_n)
        full_product.next_to(equals)
        equals2.next_to(equals, DOWN, 1.5*LARGE_BUFF)

        nudge_brace = Brace(x_dx_to_n, DOWN)
        nudged_output = nudge_brace.get_text("Nudged \\\\ output")
        product_brace = Brace(full_product, UP)
        product_brace.add(product_brace.get_text("$n$ times"))

        self.add(x_to_n)
        self.play(ShowCreation(down_arrow))
        self.play(
            FadeIn(x_dx_to_n),
            GrowFromCenter(nudge_brace),
            GrowFromCenter(nudged_output)
        )
        self.dither()
        self.play(
            Write(VGroup(equals, full_product)),
            GrowFromCenter(
                product_brace,
                rate_func = squish_rate_func(smooth, 0.6, 1)
            ),
            run_time = 3
        )
        self.dither()
        self.workout_product(equals2, full_product)

    def workout_product(self, equals, full_product):
        product_part_tex_pairs = zip(full_product, full_product.expression_parts)
        xs, dxs = [
            VGroup(*[
                submob
                for submob, tex in product_part_tex_pairs
                if tex == target_tex
            ])
            for target_tex in "x", "dx"
        ]

        x_to_n = TexMobject("x^n")
        extra_stuff = TexMobject("+(\\text{Multiple of }\\, dx^2)")
        # extra_stuff.scale(0.8)
        VGroup(*extra_stuff[-4:-2]).highlight(self.dx_color)

        x_to_n.next_to(equals, RIGHT, align_using_submobjects = True)
        x_to_n.highlight(self.x_color)

        xs_copy = xs.copy()
        full_product.save_state()
        self.play(full_product.highlight, WHITE)
        self.play(xs_copy.highlight, self.x_color)
        self.play(
            Write(equals),
            Transform(xs_copy, x_to_n)
        )
        self.dither()
        brace, derivative_term = self.pull_out_linear_terms(
            x_to_n, product_part_tex_pairs, xs, dxs
        )
        self.dither()

        circle = Circle(color = DERIVATIVE_COLOR)
        circle.replace(derivative_term, stretch = True)
        circle.scale_in_place(1.4)
        circle.rotate_in_place(
            Line(
                derivative_term.get_corner(DOWN+LEFT),
                derivative_term.get_corner(UP+RIGHT),
            ).get_angle()
        )

        extra_stuff.next_to(brace, aligned_edge = UP)

        self.play(Write(extra_stuff), full_product.restore)
        self.dither()
        self.play(ShowCreation(circle))
        self.dither()

    def pull_out_linear_terms(self, x_to_n, product_part_tex_pairs, xs, dxs):
        last_group = None
        all_linear_terms = VGroup()
        for dx_index, dx in enumerate(dxs):
            if dx is dxs[-1]:
                v_dots = TexMobject("\\vdots")
                v_dots.next_to(last_group[0], DOWN)
                h_dots_list = [
                    submob
                    for submob, tex in product_part_tex_pairs
                    if tex == "\\cdots"
                ]
                h_dots_copy = h_dots_list[0].copy()
                self.play(ReplacementTransform(
                    h_dots_copy, v_dots,
                ))
                last_group.add(v_dots)
                all_linear_terms.add(v_dots)

            dx_copy = dx.copy()
            xs_copy = xs.copy()
            xs_copy.remove(xs_copy[dx_index])
            self.play(
                dx_copy.highlight, self.dx_color,
                xs_copy.highlight, self.x_color,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )

            dx_copy.generate_target()
            xs_copy.generate_target()
            target_list = [dx_copy.target] + list(xs_copy.target)
            target_list.sort(
                lambda m1, m2 : cmp(m1.get_center()[0], m2.get_center()[0])
            )
            dots = TexMobject("+", ".", ".", "\\dots")
            for dot_index, dot in enumerate(dots):
                target_list.insert(2*dot_index, dot)
            group = VGroup(*target_list)
            group.arrange_submobjects(RIGHT, SMALL_BUFF)
            if last_group is None:
                group.next_to(x_to_n, RIGHT)
            else:
                group.next_to(last_group, DOWN, aligned_edge = LEFT)
            last_group = group

            self.play(
                MoveToTarget(dx_copy),
                MoveToTarget(xs_copy),
                Write(dots)
            )
            all_linear_terms.add(dx_copy, xs_copy, dots)

        all_linear_terms.generate_target()
        all_linear_terms.target.scale(0.7)
        brace = Brace(all_linear_terms.target, UP)
        compact = TexMobject("+\\,", "n", "x^{n-1}", "\\,dx")
        compact.highlight_by_tex("x^{n-1}", self.x_color)
        compact.highlight_by_tex("\\,dx", self.dx_color)
        compact.next_to(brace, UP)
        brace.add(compact)
        derivative_term = VGroup(*compact[1:3])

        VGroup(brace, all_linear_terms.target).shift(
            x_to_n[0].get_right()+MED_LARGE_BUFF*RIGHT - \
            compact[0].get_left()
        )

        self.play(MoveToTarget(all_linear_terms))
        self.play(Write(brace, run_time = 1))
        return brace, derivative_term

class OneOverX(PiCreatureScene, GraphScene):
    CONFIG = {
        "unit_length" : 3.0,    
        "graph_origin" : (SPACE_WIDTH - LARGE_BUFF)*LEFT + 2*DOWN,
        "rectangle_color_kwargs" : {
            "fill_color" : BLUE,
            "fill_opacity" : 0.7,
            "stroke_width" : 1,
            "stroke_color" : WHITE,
        },

        "x_axis_label" : "",
        "y_axis_label" : "",
        "x_min" : 0,
        "y_min" : 0,
        "x_tick_frequency" : 0.5,
        "y_tick_frequency" : 0.5,
        "x_labeled_nums" : range(0, 4),
        "y_labeled_nums" : [1],
        "y_axis_height" : 10,
        "morty_scale_val" : 0.8,
        "area_label_scale_factor" : 0.75,
        "dx" : 0.1,
    }
    def setup(self):
        for c in self.__class__.__bases__:
            c.setup(self)
        self.x_max = self.x_axis_width/self.unit_length
        self.y_max = self.y_axis_height/self.unit_length


    def construct(self):
        self.introduce_function()
        self.introduce_puddle()
        self.introduce_graph()
        self.perform_nudge()
        # self.draw_graph()


    def introduce_function(self):
        func = TexMobject("f(x) = ", "\\frac{1}{x}")
        func.to_edge(UP)
        recip_copy = func[1].copy()
        x_to_neg_one = TexMobject("x^{-1}")
        x_to_neg_one.submobjects.reverse()
        neg_one = VGroup(*x_to_neg_one[:2])
        neg_two = TexMobject("-2")

        self.play(
            Write(func),
            self.pi_creature.change_mode, "pondering"
        )
        self.dither()
        self.play(
            recip_copy.next_to, self.pi_creature, UP+LEFT,
            self.pi_creature.change_mode, "raise_right_hand"
        )
        x_to_neg_one.move_to(recip_copy)
        neg_two.replace(neg_one)
        self.play(ReplacementTransform(recip_copy, x_to_neg_one))
        self.dither()
        self.play(
            neg_one.scale, 1.5,
            neg_one.next_to, x_to_neg_one, LEFT, SMALL_BUFF, DOWN,
            rate_func = running_start,
            path_arc = np.pi
        )
        self.play(FadeIn(neg_two))
        self.dither(2)
        self.say(
            "More geometry!",
            target_mode = "hooray",
            added_anims = [
                FadeOut(x_to_neg_one),
                FadeOut(neg_two),
            ],
            run_time = 2
        )
        self.dither()
        self.play(*self.get_bubble_fade_anims())


    def introduce_puddle(self):
        pass

    def introduce_graph(self):
        pass

    def perform_nudge(self):
        pass


    ########

    def get_pi_creature(self):
        morty = PiCreatureScene.get_pi_creature(self)
        morty.scale(
            self.morty_scale_val, 
            about_point = morty.get_corner(DOWN+RIGHT)
        )
        return morty

    def draw_graph(self):
        self.setup_axes()
        graph = self.get_graph(lambda x : 1./x)

        rect_group = self.get_rectangle_group(0.5)

        self.add(rect_group)
        self.dither()
        self.change_rectangle_group(
            rect_group, 2,
            target_group_kwargs = {
                "x_label" : "2",
                "one_over_x_label" : "\\frac{1}{2}",
            },
            added_anims = [ShowCreation(graph)]
        )
        self.dither()

    def get_rectangle_group(
        self, x, 
        x_label = "x", 
        one_over_x_label = "\\frac{1}{x}"
        ):
        result = VGroup()
        result.x_val = x
        result.rectangle = self.get_rectangle(x)

        result.x_brace, result.dx_brace = braces = [
            Brace(result.rectangle, vect)
            for vect in UP, RIGHT
        ]
        result.labels = VGroup()
        for brace, label in zip(braces, [x_label, one_over_x_label]):
            brace.get_text("$%s$"%label)
            result.labels.add(brace.get_text("$%s$"%label))

        area_label = TextMobject("Area = 1")
        area_label.scale(self.area_label_scale_factor)
        max_width = max(result.rectangle.get_width()-2*SMALL_BUFF, 0)
        if area_label.get_width() > max_width:
            area_label.scale_to_fit_width(max_width)
        area_label.move_to(result.rectangle)
        result.area_label = area_label

        result.add(
            result.rectangle,
            result.x_brace,
            result.dx_brace,
            result.labels,
            result.area_label,
        )
        return result

    def get_rectangle(self, x):
        rectangle = Rectangle(
            width = x*self.unit_length,
            height = (1./x)*self.unit_length,
            **self.rectangle_color_kwargs
        )
        rectangle.move_to(self.graph_origin, DOWN+LEFT)
        return rectangle

    def change_rectangle_group(
        self, 
        rect_group, target_x,
        target_group_kwargs = None,
        added_anims = [],
        **anim_kwargs
        ):
        target_group_kwargs = target_group_kwargs or {}
        if "run_time" not in anim_kwargs:
            anim_kwargs["run_time"] = 3

        target_group = self.get_rectangle_group(target_x, **target_group_kwargs)
        target_labels = target_group.labels
        labels_transform = Transform(
            rect_group.labels,
            target_group.labels
        )

        start_x = float(rect_group.x_val)
        def update_rect_group(group, alpha):
            x = interpolate(start_x, target_x, alpha)
            new_group = self.get_rectangle_group(x, **target_group_kwargs)
            Transform(group, new_group).update(1)
            labels_transform.update(alpha)
            for l1, l2 in zip(rect_group.labels, new_group.labels):
                l1.move_to(l2)
            return rect_group

        self.play(
            UpdateFromAlphaFunc(rect_group, update_rect_group),
            *added_anims,
            **anim_kwargs
        )






























