from sqlalchemy import text

GET_ALL_MFP_DATA = text(
    """
            SELECT
                mfp.pore_position_id,
                shape.shape,
                porosity.porosity,
                n.normalized_misalignment,
                mfp.Thickness,
                mfp.MSD_seed_1,
                mfp.MSD_seed_2,
                mfp.MSD_seed_3,
                mfp.MSD_seed_4,
                mfp.MSD_seed_5,
                mfp.MSD_seed_6,
                mfp.MSD_seed_7,
                mfp.MSD_seed_8,
                mfp.MSD_seed_9,
                mfp.MSD_seed_10
            FROM
                pore_position_info as pf
            INNER JOIN
                shape ON shape.id = pf.shape_id
            INNER JOIN
                porosity ON porosity.id = pf.porosity_id
            INNER JOIN
                normalized_misalignment AS n ON n.id = pf.normalize_misalignment_id
            INNER JOIN
                mfp ON mfp.pore_position_id = pf.id
            """
)


GET_MFP_DATA = text(
    """
            SELECT
                mfp.pore_position_id,
                shape.shape,
                porosity.porosity,
                n.normalized_misalignment,
                mfp.Thickness,
                mfp.MSD_seed_1,
                mfp.MSD_seed_2,
                mfp.MSD_seed_3,
                mfp.MSD_seed_4,
                mfp.MSD_seed_5,
                mfp.MSD_seed_6,
                mfp.MSD_seed_7,
                mfp.MSD_seed_8,
                mfp.MSD_seed_9,
                mfp.MSD_seed_10
            FROM
                pore_position_info as pf
            INNER JOIN
                shape ON shape.id = pf.shape_id
            INNER JOIN
                porosity ON porosity.id = pf.porosity_id
            INNER JOIN
                normalized_misalignment AS n ON n.id = pf.normalize_misalignment_id
            INNER JOIN
                mfp ON mfp.pore_position_id = pf.id
            WHERE
                shape.shape = :shape AND
                porosity.porosity = :porosity AND
                n.normalized_misalignment = :normalized_misalignment;
            """
)

UPDATE_MFP_DATA = text(
    """
            UPDATE mfp
            SET
                Thickness = :thickness,
                MSD_seed_1 = :MSD_seed_1,
                MSD_seed_2 = :MSD_seed_2,
                MSD_seed_3 = :MSD_seed_3,
                MSD_seed_4 = :MSD_seed_4,
                MSD_seed_5 = :MSD_seed_5,
                MSD_seed_6 = :MSD_seed_6,
                MSD_seed_7 = :MSD_seed_7,
                MSD_seed_8 = :MSD_seed_8,
                MSD_seed_9 = :MSD_seed_9,
                MSD_seed_10 = :MSD_seed_10
            FROM
                pore_position_info pf
                INNER JOIN shape s ON s.id = pf.shape_id
                INNER JOIN porosity p ON p.id = pf.porosity_id
                INNER JOIN normalized_misalignment nm ON nm.id = pf.normalize_misalignment_id

            WHERE
                mfp.pore_position_id = pf.id
                AND s.shape = :shape
                AND p.porosity = :porosity
                AND nm.normalized_misalignment = :normalized_misalignment
        """
)

GET_PORE_INF_ID = text(
    """
        SELECT
          pf.id
        FROM
          pore_position_info as pf
        INNER JOIN
            shape ON shape.id = pf.shape_id
        INNER JOIN
            porosity ON porosity.id = pf.porosity_id
        INNER JOIN
            normalized_misalignment AS n ON n.id = pf.normalize_misalignment_id
        WHERE
            shape.shape = :shape AND
            porosity.porosity = :porosity AND
            n.normalized_misalignment = :normalized_misalignment;
        """
)
GET_ALL_PORE_POSITION_INF = text(
    """
    SELECT
      pf.id as pore_position_id,
      shape.shape,
      porosity.porosity,
      n.normalized_misalignment
    FROM
        pore_position_info as pf
    INNER JOIN
        shape ON shape.id = pf.shape_id
    INNER JOIN
        porosity ON porosity.id = pf.porosity_id
    INNER JOIN
        normalized_misalignment AS n ON n.id = pf.normalize_misalignment_id
    """
)


GET_IMG_INF = text(
    """
    SELECT
      shape.shape,
      porosity.porosity,
      n.normalized_misalignment,
      img.pixel_x_num,
      img.pixel_y_num,
      img.x_scale_length,
      img.y_scale_length,
      img.img_path
    FROM
        pore_position_info as pf
    INNER JOIN
        shape ON shape.id = pf.shape_id
    INNER JOIN
        porosity ON porosity.id = pf.porosity_id
    INNER JOIN
        normalized_misalignment AS n ON n.id = pf.normalize_misalignment_id
    INNER JOIN
        img ON img.pore_position_id = pf.id
    WHERE
        shape.shape = :shape AND
        porosity.porosity = :porosity AND
        n.normalized_misalignment = :normalized_misalignment AND
        img.pixel_x_num = :pixel_x_num AND
        img.pixel_y_num = :pixel_y_num AND
        img.x_scale_length = :x_scale_length AND
        img.pixel_x_num = :pixel_x_num AND
        img.y_scale_length = :y_scale_length;
    """
)
